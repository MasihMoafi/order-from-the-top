**This is a partial report.** I read the game design and the
requested track brief, but the paper output was truncated before
I could read all seven files in full. The findings below are
grounded in passages I could inspect; they are not a substitute
for the requested complete review. I have left unverified
experimental details open.

## Dafoe et al. — *Open Problems in Cooperative AI*

**About and result.** This is a research agenda for cooperation
between agents. It identifies four capabilities: understanding,
communication, commitment and institutions. Its central point is
that research should also examine “exclusion and coercion.”
([paper](rag-corpus/papers/dafoe2020-open-problems-cooperative-ai.txt))

**Measurement and roles.** The inspected passages present a
framework, not a new agent experiment. They do not establish an
agent count, model, scoring method or role-choice taxonomy.

**Design implication.** Log cooperation that harms outsiders as
well as cooperation within a family. The paper explicitly flags
“exclusion and collusion” as a downside. Our proposed game would
instantiate the agenda, but the inspected material does not
establish that its particular LLM experiment has been run before.

## Conitzer and Oesterheld — *Foundations of Cooperative AI*

**About and result.** This paper proposes a game-theoretic
research agenda for cooperation among advanced AI systems. Its
two-agent Traveler’s Dilemma example has “only equilibrium
… \(q_1=q_2=0\),” despite the agents’ objectives being close.
([paper](rag-corpus/papers/conitzer2023-foundations-cooperative-ai.txt))

**Measurement and roles.** The inspected example is a theoretical
two-player payoff game, with quality choices from 0 to 7; it is
not an LLM-judge evaluation. Those numbers are **actions**, not
social-role labels. I have not verified the entire paper for
other experimental details.

**Design implication.** Record individual and collective payoffs
separately: similar interests do not guarantee a good group
outcome in the paper’s example. Repeated dilemmas themselves are
not novel; the paper discusses repeated prisoner’s dilemma and
“grim trigger.” The proposed network and LLM behavior are the
features to investigate.

## Sun et al. — *Cooperative AI via Decentralized Commitment Devices*

**About and result.** This is a research agenda about credible
commitments, their implementation and their security. It calls
for “empirical testing frameworks” under “real-world commitment
constraints,” and discusses strategic mediators and exploitation.
([paper](rag-corpus/papers/sun2023-decentralized-commitment-devices.txt))

**Measurement and roles.** The inspected passages use literature
examples and a stop-light game; they do not establish a new LLM
experiment or an LLM judge. In the stop-light example, players
choose among **Fast, Caution, Stop**: these are predefined
actions, not a menu of emergent social roles.

**Design implication.** Treat a letter promising restraint and a
code-enforced commitment as distinct conditions. The paper warns
that a mediator can have an “informational advantage” and act
strategically. Our king could be studied under different
information and enforcement rules, but calling it a decentralized
commitment device would require implementing such a device.

## Haupt et al. — *Formal Contracts Mitigate Social Dilemmas in Multi-Agent Reinforcement Learning*

**About and result.** The paper studies voluntary, binding reward
transfers between agents. It reports a theoretical result for
fully observable Markov games under a “sufficiently rich space of
contracts,” and tests a training method in several game domains.
([paper](rag-corpus/papers/haupt2022-formal-contracts-marl.txt))

**Measurement and roles.** The abstract names static games and
domains for traffic, pollution and common-pool resources. Its
Cleanup illustration says “one agent commits to ‘pay’ the other
to clean the river.” This is an example of task specialization,
not evidence from the inspected text of a free-choice role menu.
The full experimental counts, model details and scoring procedure
remain unverified here.

**Design implication.** Compare voluntary binding transfers with
ordinary promises, then track who pays, cleans, benefits and
defects. A commons game with specialization overlaps
conceptually with Cleanup; the proposed hierarchical LLM setting
would differ, but the novelty claim needs the full comparison.

## Ivanov et al. — *Mediated Multi-Agent Reinforcement Learning*

**About and result.** The paper trains a benevolent mediator
alongside agents and defines cooperation in terms of a socially
beneficial equilibrium. It reports that naively maximizing
social welfare can lead agents to refuse mediation; it considers
their incentives to address that problem.
([paper](rag-corpus/papers/ivanov2023-mediated-marl.txt))

**Measurement and roles.** The inspected text describes
prisoner’s-dilemma variants and public-goods games, including
one-shot and sequential games, with policy-gradient training.
Agents choose whether to **commit** to a mediator, which “may
act on behalf of agents” that agree. The mediator is a
researcher-defined role; commit is an available action, not a
free-form social role. Exact experimental counts and scoring
details still need verification.

**Design implication.** If the king mediates, record whether
agents can refuse its intervention and what each gains from
accepting or refusing. The paper’s mediator is “benevolent”;
our king’s behavior and incentives should be specified and
measured before claiming a difference.

## Ramírez et al. — *Game Manipulators: The Strategic Implications of Binding Contracts*

**About and result.** This paper studies players or outside
manipulators who use binding offers to change a game’s payoffs
and extract fees. Its abstract says such offers can lead to an
equilibrium with “potentially lower payoffs for the players.”
([paper](rag-corpus/papers/game-manipulators-binding-contracts.txt))

**Measurement and roles.** The paper describes theoretical
scenarios and simulations of regret-minimizing agents. It
distinguishes a player making an offer, an external manipulator,
counteroffers and a second external manipulator. These are
defined positions in scenarios, not evidence of agents freely
inventing roles. I have not verified all simulation settings or
scoring details.

**Design implication.** Log threats, contingent offers, fees and
counteroffers separately from their outcomes. A mafia boss
demanding payment under an enforceable threat overlaps with the
paper’s “pay me a fee, or I will distort the payoff matrices”
mechanism. A natural-language threat without binding enforcement
would test a different commitment condition.

## Landis and Schwartzbach — *Stackelberg Attacks on Auctions and Blockchain Transaction Fee Mechanisms*

**About and result.** This theoretical paper studies auctions
where agents can commit to strategies. Under its stated
conditions, an attacker can obtain an item essentially free
while other agents enter a lottery, harming auctioneer revenue.
([paper](rag-corpus/papers/stackelberg-attacks-auctions.txt))

**Measurement and roles.** The model has \(n\) agents and \(m\)
identical items; the paper illustrates three agents competing
for two slots. It assumes rational, risk-neutral agents and
studies utilities and equilibrium. The “leading contract agent”
is a defined strategic position; bids and commitments are
actions. The inspected analysis is theoretical, rather than an
LLM-judge experiment.

**Design implication.** Measure individual gains and losses to
the institution separately when agents coordinate. This paper’s
auction has multiple identical items and binding contracts; our
proposed dollar auction has different rules. Do not describe its
result as a finding about dollar auctions.

## For our design

### 1. Free roles or a numbered menu?

The inspected papers distinguish **available actions** and
**defined institutional positions**—such as mediator,
manipulator and bidder. Their numbered choices do not establish a
recommendation to give LLM agents numbered social roles.

**Recommendation:** keep social roles unnamed and unassigned in
the main condition, while giving agents the actions needed to
act: send a letter, make a proposal, accept, refuse, and so on.
Classify behavior afterward from observable events. A numbered
role menu could be a separate comparison condition.

There is one important qualification: the design already assigns
formal positions. Leaders have special communication and war
powers, the god sits above them, and the mafia family has a boss.
Those formal offices cannot themselves be presented as emergent.
Measure instead whether *informal influence* emerges within or
across those positions: whose proposals are followed, who
mediates, and who directs others without an assigned office.

### 2. Closest prior works to compare

From the passages inspected, the strongest **provisional**
comparisons are:

1. **Haupt et al.** — binding transfers, social dilemmas and
   common resources.
2. **Ivanov et al.** — a mediator, voluntary participation and
   individual incentives.
3. **Ramírez et al.** — threats, binding offers and manipulation.
4. **Landis and Schwartzbach** — commitment-enabled coordination
   that harms an institution.
5. **Conitzer and Oesterheld** — repeated dilemmas and
   misalignment arising from interaction.

These are the closest among the assigned papers based on the
passages inspected, not a verified ranking of all prior work.

### 3. Measures to copy or adapt

- **Individual payoff and total welfare:** Ivanov describes
  social welfare as an aggregate, “usually, the sum total,” of
  cumulative rewards. Keep the individual scores too.
- **Participation and refusal:** Ivanov’s agents can decline the
  mediator. Log acceptance, refusal and resulting payoffs if our
  design provides an equivalent choice.
- **Payoff from cooperation versus defiance:** Landis and
  Schwartzbach define a “price of defiance” as the ratio of
  cooperating utility to deviating utility. Adapt this only where
  both quantities can be defined and estimated.
- **Commitment and breach:** distinguish an unenforced promise
  from a binding commitment, following Sun et al.’s focus on
  “real-world commitment constraints.”
- **Influence and specialization:** the game design already
  proposes logging orders, followed proposals, mediation,
  sacrifice and defection. These are useful proposed measures,
  but the inspected papers do not validate that taxonomy.

The unfinished step is the full, untruncated reading of all seven
papers, especially their methods and appendices, before treating
agent counts, model details, scoring methods or novelty risks as
complete.