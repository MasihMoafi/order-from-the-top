I could not complete the requested full reading of all four papers.
The report below is based on selected passages, so its novelty assessment
is **provisional** and should not be treated as a complete literature
review.

## Akata et al. — *Playing repeated games with large language models*

**About and result.** The paper studies two-player repeated games:
cooperation, defection and coordination across payoff structures.
Its authors report that models did well in self-interested games but
“behave suboptimally in games that require coordination.” In their
Prisoner’s Dilemma setup, GPT-4 “never cooperates again” with an
opponent that defects once and then cooperates.
[Paper, pp. 1380–1382](rag-corpus/papers/akata2025-repeated-games-llms.txt)

**Setup and measurement.** Two players choose between two actions
over ten rounds. The models include GPT-4, text-davinci-002,
text-davinci-003, Claude 2 and Llama 2 70B; some comparisons use
hand-coded strategies or humans. The paper measures, among other
things, defection and coordination rates and “score divided by maximum
score achievable under ideal conditions.” Payoffs follow the game
matrix; the reported game score is calculated, not an LLM’s judgment.
[Paper, pp. 1381–1383](rag-corpus/papers/akata2025-repeated-games-llms.txt)

**Roles and taxonomy.** Players receive a fixed **action menu**, not
a menu of social roles. The paper also supplies hand-coded opponents
that always cooperate, always defect, or defect once and then
cooperate. Its six game families are win–win, biased, second-best,
cyclic, unfair and Prisoner’s Dilemma. These classify games, not
emergent agent roles.
[Paper, pp. 1381–1382](rag-corpus/papers/akata2025-repeated-games-llms.txt)

**Implication and novelty.** Copy the repeated-game baseline, including
a one-time-defection opponent, and measure whether agents retaliate
and forgive. Repeated LLM Prisoner’s Dilemma alone would repeat this
work. Your possible distinction is how such behavior travels through
hierarchies and affects faction survival.

## Piatti et al. — *Cooperate or Collapse*

**About and result.** GovSim studies whether a community of LLM agents
can sustain a shared resource while each extracts from it. It uses
fishery, pasture and pollution settings. The paper reports that the
best model’s full-run survival rate was **53.3%**, and that
communication and “universalization”-based reasoning improved
sustainability in the tested conditions.
[Paper, abstract and §3](rag-corpus/papers/piatti2024-govsim-cooperate-or-collapse.txt)

**Setup and measurement.** Five agents share a resource for up to
12 simulated months. They privately select extraction amounts, those
actions execute simultaneously, and agents then discuss freely.
The paper tests 15 named open- and closed-weight LLMs, with five
random seeds per simulation. It calculates survival time and rate,
individual gain, efficiency, equality and overuse from the simulated
state. Dialogue classification is different: **GPT-4-turbo** assigns
utterances to categories; one author agreed with it on **72%** of
100 sampled utterances.
[Paper, §§2–3](rag-corpus/papers/piatti2024-govsim-cooperate-or-collapse.txt)

**Roles and taxonomy.** Agents have assigned scenario identities,
such as fishermen, shepherds or factory owners, and identical
instructions designed to avoid priming them as “cooperative or greedy.”
They choose extraction amounts and speak freely; they do not choose
from a social-role menu. The paper classifies utterances into:

1. **Information:** sharing facts, identifying problems, proposing
   solutions.
2. **Negotiation:** persuasion, consensus seeking, disagreement.
3. **Relational:** excusing behavior, punishment.

These are labels applied **after** agents speak, not roles assigned
to agents.
[Paper, §§3.1 and 3.6](rag-corpus/papers/piatti2024-govsim-cooperate-or-collapse.txt)

**Implication and novelty.** The proposed commons faction has a
direct predecessor. Use GovSim’s resource and inequality metrics,
and compare communication with no communication. Differ through the
effect of commons outcomes on a faction’s position in a larger
hierarchy and war. Treat dialogue labels as annotations: the paper’s
LLM classifier did not have perfect human agreement.

## Park et al. — *Generative Agents*

**About and result.** The paper builds a simulated town of agents with
memory, reflection and planning. It evaluates individual believability
and collective information spread, relationship formation and
coordination. In one two-day simulation, knowledge of a party spread
from one agent to 13, and five of 12 invited agents attended.
[Paper, §§6–7](rag-corpus/papers/park2023-generative-agents.txt)

**Setup and measurement.** The town contains **25 agents** using
`gpt3.5-turbo`. In a controlled evaluation, **100 human evaluators**
ranked interview responses from the full architecture, three ablated
versions and a human-authored condition. For the town run, researchers
interviewed agents, checked affirmative claims against memory records,
measured mutual-knowledge network density and counted attendance.
Believability was **human judged**, while the reported collective
measures combined labeled interviews, record checks and counts.
[Paper, §§4 and 6–7](rag-corpus/papers/park2023-generative-agents.txt)

**Roles and taxonomy.** Agents have authored identities and life
contexts. Isabella is initialized with the intent to organize a party;
the subsequent invitations and attendance arise through interaction.
That is a seeded organizer, not evidence that an unassigned leader
emerged. The paper’s collective categories are **information
diffusion, relationship formation and coordination**, rather than a
numbered menu of agent roles.
[Paper, §§3 and 7](rag-corpus/papers/park2023-generative-agents.txt)

**Implication and novelty.** Trace a letter or proposal from sender to
recipients, then check both what agents say they know and what they
actually do. Park already studies open-ended social coordination and
information diffusion. Your distinction would be testing these under
explicit survival incentives, restricted communication and hierarchical
failure.

## Vezhnevets et al. — *Concordia technical report*

**About and result.** Concordia is a library for building
language-mediated agent simulations. Agents describe intended actions
in natural language; a “Game Master” translates them into environmental
effects. Its main contribution is the framework and its examples,
rather than a single measured result comparable to a game benchmark.
[Paper, abstract](rag-corpus/papers/vezhnevets2023-concordia-tech-report.txt)

**Setup and measurement.** Example scenarios include a two-player
calendar task and a five-player election. The report describes a
configurable Game Master that maintains state, checks validity and
“decid[es] the effect of agents’ actions.” The passages inspected do
not establish one model, agent count or scoring method for the whole
framework. In particular, its language-mediated adjudication should
not be described as uniformly code-scored.
[Paper, §2 and appendix examples](rag-corpus/papers/vezhnevets2023-concordia-tech-report.txt)

**Roles and taxonomy.** The election example assigns two candidates
and an agent “trying to ruin Alice’s reputation with disinformation”;
the other two have voting as their agenda. Actions are expressed
in natural language, and agent identities and components are
configurable. These examples seed social functions rather than
demonstrate that all such functions emerged freely.
[Paper, appendix examples](rag-corpus/papers/vezhnevets2023-concordia-tech-report.txt)

**Implication and novelty.** The Game Master resembles your central
orchestrator in broad form, but your design can make a sharper
distinction: calculate game state, death and payoffs with code, while
letting agents deliberate in language. Concordia already provides
general social simulation and a central environment manager; those
features alone are not a novelty claim.

## For our design

### 1. Free roles or a numbered menu?

The papers distinguish **action constraints** from **social roles**.
Akata fixes the actions; GovSim fixes the extraction mechanism but
allows free discussion; Park and Concordia seed identities or
objectives. GovSim applies its eight dialogue categories afterward.

**Recommendation: keep social roles free in the main condition.**
Give agents the game rules and valid actions, then classify observable
behavior afterward. That fits Track 2’s question about how roles
emerge. A numbered role menu would make agents’ selections easier to
count, but would seed the very roles being studied.

There is one qualification: the proposed tree already assigns
structural positions, and only faction leaders can negotiate across
factions. Measure **emergent influence within those constraints**;
do not claim that the formal leadership positions themselves emerged.

### 2. Closest prior work to cite and differ from

1. **Piatti et al.** — closest to the commons subgame, free discussion
   and collapse. Differ by connecting resource outcomes to hierarchy
   and inter-faction conflict.
2. **Akata et al.** — closest to the repeated-game and defection
   baseline. Differ by measuring consequences beyond the pair.
3. **Park et al.** — closest to social diffusion and coordination.
   Differ through incentives, communication restrictions and failures.
4. **Vezhnevets et al.** — relevant to the simulation architecture
   and central Game Master. Explain your code-adjudicated rules.

These are the closest **among the four assigned papers**, based on
the passages inspected; this is not a claim about all prior work.

### 3. Measures to copy

- **From Akata:** defection rate, action history, accumulated payoff
  and normalized payoff; include a one-time defector to test
  retaliation and forgiveness.
- **From GovSim:** survival time, full-run survival rate, individual
  gains, efficiency, equality and overuse. Run a communication
  ablation if the experiment budget permits.
- **From Park:** information diffusion paths, fraction informed,
  relationship-network density and the gap between an invitation
  or stated intention and an observed action. Check claims against
  event records.

For your own role analysis, count orders, proposals followed,
mediation, sacrifice and defection from logs as the design note
proposes. Define these measures before the run, and distinguish a
formal leader’s authority from influence earned in interaction.