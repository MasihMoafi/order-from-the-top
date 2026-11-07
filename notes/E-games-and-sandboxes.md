# Swarm hackathon plan (draft, 6 Nov evening)

Track 2 (Science of Agent Networks), with Track 4 (oversight).

## Goal

Not to make agents escape. OpenShell already contains each agent.
The goal: find **when a group of agents that are each safe tips into
breaking the rules together**, and **which rule of the game stops it**.

## Why (the evidence)

- HF incident: over 90% of the 533 agents on the board joined
  (METR, Figure 11). No agent was told to.
- Dafoe et al. 2020, §5.1: cooperation can be harmful, "students
  sharing answers during examinations". HF was that: good teamwork,
  aimed against the scorer.
- Art of Strategy ch. 9, "Faster than a speeding ticket": if few break
  a rule, each gets caught; if many do, the police can't stop them
  all. So there are two stable states (nobody, everybody) and a tipping
  point between them. Ch. 9 recap: a "critical mass" flips the group.
- Dafoe §3.3 "planner perspective": which structures steer a group
  away from a bad equilibrium? That is our defence question.

## The games (many agents, rules enforced in code)

**G1 Speeding game (main).** N = 20 to 50 agents, each with a task it
cannot finish. A shared board. Posting or using a shortcut breaks the
rules. A monitor can catch only k agents per round (safety in numbers).
- Vary: planted rule-breakers m (Sepehr's idea C), monitor capacity k,
  who sees whom (all vs at most 5 neighbours).
- Measure: share of agents breaking the rule each round; the m at which
  the group tips; whether the change is sudden or gradual.

**G2 Threats and promises (defences).** Same game, with the overseer's
rule changed (Art of Strategy ch. 6 and 7; Dafoe §4.3 and §4.4):
- a threat (caught = removed) vs a promise (reward for reporting);
- a credible threat (punishment really happens) vs an empty one;
- reputation shown on the board vs hidden.
- Measure: how much each one moves the tipping point.

## Where your past work fits (arms, not separate projects)

- EWS Finding 1 (simulation framing, 78 to 97 of 100): tell half the
  agents "this is a simulation". Does the group tip sooner?
- EWS channel split: count agents that refuse in words but break the
  rule in their actions.
- Chronos: put the rule-breakers' posts first vs last on the board.
  Does order move the tipping point?

## Borrowed from the Kaggle winners

- HostileShop: score by game state (who posted), not by an LLM judge.
- Sweet Harmony: fixed seeds, repeated runs, confidence intervals.
- Mind the Gap: some failures appear only in agent runs, not in chat.
- Judges' theme: saying no in text while acting through the tool.

## Rubric check (RUBRIC.md)

- Impact: a measured tipping point of harmful cooperation and a
  tested fix, tied to a real incident.
- Execution: counts from code, at least 4 seeds per setting, intervals.
- Clarity: one figure per question.
- Closest prior work to cite and beat: Magistrali & Shani (committed
  minority capture), GovSim (commons game), Prompt Infection.
- Mark any reused code "preexisting".

## Tools

- Models: through the Adaption API (key at ~/.config/adaption/api_key).
  DeepSeek V4 Flash is the cheapest; add Qwen or Gemma to compare.
- Harness: a small Python loop; the game rules live in code so nobody
  (no LLM Game Master) can fake an outcome. Full logs per agent.

## Read properly (in this order)

1. METR HF report, pp. 5 to 16.
2. Art of Strategy ch. 9 (speeding, Schelling's tipping), ch. 6 and 7.
3. Dafoe et al. §5.1, §3.3, §4.3, §4.4.
4. GovSim (Piatti 2024): the closest many-agent game.

## Decided

Sepehr's decomposition study (Design B) is dropped (6 Nov).

## Sandboxes in plain words

- A sandbox is a closed box that an agent's code runs in. OpenShell
  limits three things per box: which files it may touch (Landlock),
  which system calls it may make (seccomp), and which websites it may
  reach (a network proxy).
- At HF each box held. The hole was a service all boxes shared (a
  package cache), which became a message board (METR p. 5).
- OpenShell checks each box alone; it does not check what many boxes
  do together (its prover README, "What the prover does not decide").
  Our games study exactly that "together" part.

## Games from The Art of Strategy (ch. 3, 4, 9) for many agents

Each game names its HF parallel. Rules and payoffs live in code.

1. **Many-player dilemma** (ch. 3, Battalio's 27 students): each who
   defects gains 46 cents, everyone else loses 4. HF: each agent gains
   by the shortcut, the group (and the evaluator) loses.
2. **Contribution game with costly punishment** (ch. 3): after giving,
   players may pay to fine free riders; this raised giving a lot in
   human studies. Do LLM agents punish rule-breakers?
3. **Repeated dilemma** (ch. 3, Axelrod): tit for tat, noise, tit for
   two tats. Does reputation keep agents honest?
4. **Shadow of the future** (ch. 3): a known last round invites
   cheating at the end. Tell agents when the evaluation ends, or not.
5. **Commons with Ostrom's rules** (ch. 3): clear membership, clear
   rules, graduated fines, detection built into routine. Each rule is
   a defence we can switch on.
6. **Stag hunt and focal points** (ch. 4): can agents agree on a plan
   without talking? That is tacit collusion.
7. **Chicken and battle of the sexes** (ch. 4): mixed interests; who
   commits first wins.
8. **Speeding game** (ch. 9, main game): safety in numbers, two stable
   states, a tipping point. HF: over 90% joined.
9. **Rat race** (ch. 9, bell curve): ranking agents against each other
   makes all of them push harder; a cartel cuts effort.
10. **Schelling tipping** (ch. 9, "Why did they leave?"): each agent
    has a threshold; mixed groups flip all the way.
11. **Threats, promises, credibility** (ch. 6, 7): the overseer's tools.
12. **Bridge toll** (ch. 9): price a shared resource so overuse costs.

Already done with LLMs (cite, don't repeat): repeated games (Akata),
commons (GovSim). New here: a rule-breaking game against an overseer
with limited monitors, tied to HF, and which fix moves the tip point.
