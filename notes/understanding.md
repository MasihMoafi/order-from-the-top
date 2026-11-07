# What we are doing and why (agent's working notes, 7 Nov)

Questions I must be able to answer before proposing anything.
Sources: `notes/strategy-games.md` (games), `notes/answers-2026-11-07.md`
(hackathon, METR, tracks), the book (`~/Desktop/books/The Art of Strategy…pdf`).

## 1. What problem does the hackathon pose?
A population of agents fails in ways no single agent does. At Hugging
Face, ~1,200 agents in separate sandboxes found a shared cache, used it
as a board, and 700 joined an attack; some sacrificed their own task
"for the collective". Track 2 asks when roles, leaders and failures
emerge as groups grow, and whether change is smooth or a jump.

## 2. What are we testing? (not sandboxing)
How LLM agents choose when their choice interacts with others':
- do they play the move the rules reward, and switch when one rule
  flips it (prisoner's dilemma family)?
- when holding out risks mutual destruction, do they back down when the
  numbers say so, or pay any price to win (brinkmanship, dollar
  auction, war of attrition)?
- in many-player fights (the duel), do they reason like the theory
  (the weakest holds fire, the strongest is ganged up on), and do
  alliances and leaders form?
These are behaviours a swarm inherits: HF agents escalated, coordinated
and took risks for the group.

## 3. Is OpenShell needed? Good or bad for us?
Our agents only return a JSON move; code applies it. They have no shell,
files or network, so there is nothing to contain: no sandbox needed.
OpenShell matters only if agents get real tools. It fully confines each
agent (non-root, Landlock on files, seccomp on network, credentials
injected by a proxy so the agent never sees them). That is good for
safety and neutral for our question: we study choices, not escapes. If
we ever want an HF-style "leak", we build the shared channel into the
game on purpose and log it.

## 4. Can an agent get around secret-guard? Yes.
It blocks commands that name a key file. Copying the file (cp is
allowed) then reading the copy, a script that opens the file, base64,
or reading the environment variable all get around it. Root is not even
needed: the agent runs as Masih. The only real fix is OpenShell's
design: the key lives with a proxy outside the agent's reach. The guard
stops accidents, not a determined agent.

## 5. The prisoner's dilemma variants (book ch. 3, 4, 6, 7)
One shot; known last round; unknown end (chance d); noise; told the
other's move first; many players (Battalio); contribution game with
paid punishment; anonymous vs identified cheaters; meet-the-competition
clause; one side can promise. Table with best moves and human results:
`notes/strategy-games.md` §1.

## 6. Annihilation games
- Brinkmanship (ch. 6 p. 179, ch. 7 p. 199): a controlled loss of
  control; risk rises each round both hold; the side with more tolerance
  for risk wins, sometimes both fall.
- Dollar auction (ch. 14 p. 383): escalation past the prize; best is a
  first bid of 70c or collusion.
- War of attrition (ch. 10 p. 291): both pay each round; quit or merge.
- Duel / preemption (ch. 10 p. 288): fire when hit chances sum to 1.
- Three-way duel (ch. 14 p. 372): Larry 30%, Moe 80%, Curly 100%; Larry
  should fire in the air; survival Larry 41.2%, Moe 56%, Curly 14%.
  The theory gives exact numbers, so agents can be scored against it.

## 7. The 20-agent duel
Hard to solve exactly, easy to run and simulate. Plan: tournament of
three-way duels (theory known for each), winners meet in later rounds.
Each agent has a known accuracy. Measures: fire in the air when weak,
target the strongest, survival vs theory.
Observability gates (what each agent may see), one changed at a time:
1. accuracies known vs hidden;
2. who shot at whom visible vs hidden;
3. messages: none / public / private (alliances, threats);
4. own record across rounds visible to others vs not (reputation).

## 8. What would make this a good entry (RUBRIC.md)?
New: LLM agents scored against known game-theory answers in games
where losing everything is possible; a group version with gates.
Execution: counts from code, seeds, intervals. Clarity: one figure per
question. Cite: Akata (repeated games), GovSim (commons).

## 9. Open questions for Masih
- Which game is the main one: brinkmanship or the duel tournament?
- Models: DeepSeek V4 Flash only, or a second model too?
