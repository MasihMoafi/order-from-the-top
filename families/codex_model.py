"""Adapt the signed-in Codex CLI to the engine's model response fields.

Requires Codex and bubblewrap. Calls use a temporary working directory, replace
Codex's system instructions, ignore its user config, and hide global agent
instructions inside the subprocess view without changing their source files.
Starts are spaced by gap and simultaneous calls are bounded by concurrency.
Failed calls retry within PATIENCE before raising ModelOutage.
"""

import asyncio
import json
import os
import tempfile
import time
from pathlib import Path

from .models import PATIENCE, ModelOutage, RealModel

HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
LUNA = {"model": "gpt-6-luna", "think_cap": 8000, "effort": "low"}
QUIET = (  # Codex's own extra instructions, off: players see only our prompt
    "include_permissions_instructions",
    "include_apps_instructions",
    "include_apps_usage_instructions",
    "include_skills_usage_instructions",
    "include_plugin_usage_instructions",
    "include_collaboration_mode_instructions",
)
TIMEOUT = 300  # seconds one Codex process may take


def parse(stdout):
    """Return (text, reasoning, usage, error) from Codex JSONL.

    Ignore non-JSON lines. Keep the last agent message, usage and error, and
    join reasoning items in order; absent fields have empty defaults.
    """
    text, reasoning, usage, error = "", [], {}, ""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        item = event.get("item") or {}
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "agent_message"
        ):
            text = item.get("text", "")
        elif event.get("type") == "item.completed" and item.get("type") == "reasoning":
            reasoning.append(item.get("text", ""))
        elif event.get("type") == "turn.completed":
            usage = event.get("usage") or {}
        elif event.get("type") in ("error", "turn.failed"):
            error = json.dumps(event)[:500]
    return text, "\n".join(reasoning), usage, error


class CodexModel(RealModel):
    """Provide paced CLI calls using the engine response fields and outage errors."""

    def __init__(self, home=HOME, concurrency=4, gap=2.0):
        self.home, self.gap = str(home), gap
        # Each global instructions file, resolved through symlinks, reads as empty in the view.
        names = ("AGENTS.md", "AGENTS.override.md")
        hidden = [
            os.path.realpath(Path(home) / n) for n in names if (Path(home) / n).exists()
        ]
        self.view = ["bwrap", "--dev-bind", "/", "/"]
        for path in hidden:
            self.view += ["--ro-bind", "/dev/null", path]
        self.view.append("--")
        self.sem = asyncio.Semaphore(concurrency)
        self.pace = asyncio.Lock()
        self.next_start = 0.0

    async def call(self, system, user, rng, settings=None):
        """Return the first successful response, retrying failures within PATIENCE.

        Raise ModelOutage when no retry fits the remaining patience window.
        Subprocess startup errors propagate without retry.
        """
        settings = settings or LUNA
        loop = asyncio.get_running_loop()
        async with self.sem:
            async with self.pace:
                wait = self.next_start - loop.time()
                if wait > 0:
                    await asyncio.sleep(wait)
                self.next_start = loop.time() + self.gap
            deadline, delay = loop.time() + PATIENCE, 30
            while True:
                result = await self.once(system, user, settings)
                if result["ok"]:
                    return result
                if loop.time() + delay > deadline:
                    raise ModelOutage(result["error"] or "codex call failed")
                print(f"codex retry in {delay} s: {result['error'][:200]}", flush=True)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 300)

    async def once(self, system, user, settings):
        """Return one CLI response with text, reasoning, usage and latency.

        Timeouts kill the process and return ok=False; empty replies or nonzero
        exits also return ok=False. Process startup errors propagate.
        """
        with tempfile.TemporaryDirectory(prefix="luna-") as work:
            instructions = Path(work) / "system.md"
            instructions.write_text(system)
            command = [
                *self.view,
                "codex",
                "exec",
                "--json",
                "--ephemeral",
                "--skip-git-repo-check",
                "--ignore-user-config",
                "-s",
                "read-only",
                "-m",
                settings["model"],
                "-c",
                f"model_reasoning_effort={settings['effort']}",
                "-c",
                f"model_instructions_file={instructions}",
                "-c",
                "project_doc_max_bytes=0",
                *[x for key in QUIET for x in ("-c", f"{key}=false")],
                "-",
            ]
            start = time.monotonic()
            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=work,
                env={**os.environ, "CODEX_HOME": self.home},
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                out, err = await asyncio.wait_for(
                    process.communicate(user.encode()), TIMEOUT
                )
            except TimeoutError:
                process.kill()
                await process.wait()
                return {"ok": False, "text": "", "error": f"timeout after {TIMEOUT} s"}
        text, reasoning, usage, error = parse(out.decode(errors="replace"))
        ok = process.returncode == 0 and bool(text.strip())
        if not ok and not error:
            error = f"exit {process.returncode}: {err.decode(errors='replace')[-300:]}"
        return {
            "ok": ok,
            "text": text,
            "reasoning": reasoning,
            "error": error,
            "usage": {"cost": 0, **usage},
            "latency_ms": round((time.monotonic() - start) * 1000),
        }
