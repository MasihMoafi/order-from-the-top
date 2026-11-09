"""The locked box for agents' shell tools: root over their own world, no network, nothing else."""

import asyncio
import json
import shlex
from pathlib import Path

LIMIT = 1500  # characters of output an agent reads back
SECONDS = 8  # a command is killed after this long
RUNNING = asyncio.Semaphore(6)  # commands at once on a small server


def bash_for(call: dict[str, str]) -> str:
    """Return the bash command for one shell tool call; ValueError if it is malformed."""
    arguments = json.loads(call["arguments"] or "{}")
    name = call["name"]
    if name == "bash":
        return str(arguments["command"])
    path = shlex.quote(str(arguments["path"]))
    if name == "read_file":
        return f"head -c {LIMIT} -- {path}"
    if name == "delete_file":
        return f"rm -rf -- {path}"
    if name == "write_file":
        body = shlex.quote(str(arguments["content"]))
        return f'mkdir -p -- "$(dirname -- {path})" && printf %s {body} > {path}'
    raise ValueError(f"not a shell tool: {name}")


def box_command(world: Path, home: str, command: str) -> list[str]:
    """Return the bubblewrap command: fake root, no network, only /world writable."""
    return [
        "bwrap",
        "--unshare-all",
        "--uid",
        "0",
        "--gid",
        "0",
        "--die-with-parent",
        "--new-session",
        "--ro-bind",
        "/usr",
        "/usr",
        "--symlink",
        "usr/bin",
        "/bin",
        "--symlink",
        "usr/lib",
        "/lib",
        "--symlink",
        "usr/lib64",
        "/lib64",
        "--proc",
        "/proc",
        "--dev",
        "/dev",
        "--tmpfs",
        "/tmp",
        "--bind",
        str(world),
        "/world",
        "--chdir",
        home,
        "--clearenv",
        "--setenv",
        "PATH",
        "/usr/bin:/bin",
        "--setenv",
        "HOME",
        home,
        "bash",
        "-c",
        command,
    ]


async def run_in_box(world: Path, agent: str, call: dict[str, str]) -> str:
    """Run one shell tool call and return what the agent sees: output and exit code."""
    (world / "agents" / agent).mkdir(parents=True, exist_ok=True)
    (world / "shared").mkdir(exist_ok=True)
    try:
        command = bash_for(call)
    except (ValueError, KeyError, TypeError) as exc:
        return f"error: {exc}"
    async with RUNNING:
        process = await asyncio.create_subprocess_exec(
            *box_command(world.resolve(), f"/world/agents/{agent}", command),
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        try:
            output, _ = await asyncio.wait_for(process.communicate(), SECONDS)
        except TimeoutError:
            process.kill()
            await process.wait()
            return f"error: killed after {SECONDS} seconds"
    return f"{output[:LIMIT].decode(errors='replace')}\n[exit {process.returncode}]"
