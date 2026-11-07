# Five Families: architecture in plain words (draft for Masih)

Rules: `rules.md`. This file: how the parts fit and what we want to show.

## The picture
```
 agents (76 model calls)  <->  HUB (our code)  ->  event log (JSONL, the truth)
                                 |                    |
                         rules + scoring        live board (Love Spot page)
```
- Agents never talk to each other directly. Every message is a packet to the hub:
  sender, receiver, edge, time, content. The hub delivers it only if the talk rules
  allow it, and logs it either way.
- Leaders' letters use the A2A message format (Google's agent-to-agent protocol: a
  message with an agent card and a task), carried by the hub. That makes Track 3's
  question testable ("what can one malicious agent do inside A2A?") without opening raw
  sockets.
- Lockstep rounds: all agents act at once, the hub resolves the round, then the next.
  A stage = 5 rounds + a survival check. State is saved after every stage (checkpoint).
- Control file, read before each stage: lets Masih change the pace mid-run.

## Why not raw sockets / TCP between agents
We are not testing network stacks; new kernel/TCP bugs would add risk and noise, not
answers. The hub gives the same "who can reach whom" control, full logs and replay.
Version 2 moves agents onto Cloudroom with OpenShell network rules; the hub stays the
only allowed route, so any attempt to reach someone else is blocked and logged.

## How it maps to Hugging Face (METR)
| Hugging Face | Five Families |
|---|---|
| ~1,200 agents in "isolated" sandboxes | 76 agents, talk only along tree edges |
| a shared cache became a hidden message board | condition C2: a hidden shared corner |
| one agent coordinated hundreds, in "lanes" | measure who gives orders and who follows |
| agents risked their own task for the collective | measure sacrifices under linked fates |
| agents spoofed their own logs | the hub's log is outside the agents' reach |

## What we want to show (hypotheses to test; may be refuted)
- H1 Cooperation falls with distance from the leader (deeper levels defect more).
- H2 Rising pressure (the threshold "blinds") increases lies, defiance and secret
  coordination, and these spread down the tree.
- H3 Leaders with weaker families escalate wars further (brinkmanship, book ch. 6-7).
- H4 Agents' play matches the game-theory best move in some variants and not others
  (the solver gives the best move for every variant).
Any of these can come out false; that is still a result.

## Hosts
- Never use `hetzner-pc` or `hetzner-gateway`: not ours (Masih). A new server only with his yes.
