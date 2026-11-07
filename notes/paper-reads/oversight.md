**This is a preliminary report, not the requested full-paper
review.** I read the game design and track brief, but I did not
finish reading all eight papers in full. The findings below are
limited to passages I inspected; I cannot yet certify the
role taxonomies, complete methods, or closest-prior-work ranking.

## Motwani et al. — Secret Collusion among AI Agents

**About and result.** The paper defines secret collusion as
agents using steganography to conceal coordination. It reports
“rising steganographic capabilities” and limitations in
“monitoring, paraphrasing, and parameter optimization.”
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/motwani2024-secret-collusion.txt:16)

**Methods and roles.** One experiment used two
GPT-3.5-Turbo hiring agents with assigned responsibilities:
academic and professional experience. The authors say that,
without an overseer, the agents conveyed information indirectly;
with a monitor, the tested models lacked the ability to complete
the final covert one-bit task. This is an assigned-task setting,
not free role emergence.
[Paper, appendix J.2.1](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/motwani2024-secret-collusion.txt:2801)

**Design implication and novelty.** Separate an uninstructed
condition from a condition that teaches a code. Measure whether
agents coordinate successfully *and* whether a monitor detects
it. Secret communication alone overlaps with this paper; the
family hierarchy and emergent leadership offer a different
question.

## Rose et al. — Detecting Multi-Agent Collusion Through Multi-Agent Interpretability

**About and result.** The paper uses internal model activations
to detect collusion by unknown subgroups. On its instructed
steganography task, the best method for each of four models
reached “0.99 to 1.00 AUROC”; transfer to third-party emergent
collusion was only partial.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/rose2026-detecting-collusion-interpretability.txt:27)

**Methods and roles.** The benchmark has committee scenarios,
transfer tasks and steganographic blackjack. It compares
group-level statistics and heuristics, with transcript-level LLM
judges as a comparator. The authors distinguish “instructed and
emergent collusion”; they report that only 2 of 229 collusive
episodes in one emergent setting verbalised coordination.
I have not verified the full agent counts, model list or role
prompts.
[Paper, introduction](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/rose2026-detecting-collusion-interpretability.txt:95)

**Design implication and novelty.** Keep instructed and
uninstructed coordination separate. Record both the observable
messages and the game actions: absence of an explicit agreement
does not establish absence of coordination. An oversight
experiment focused only on detecting collusion would overlap;
leadership and failure cascades in a changing hierarchy are a
different emphasis.

## Greenblatt et al. — AI Control

**About and result.** This paper tests safety protocols against
intentional subversion in programming tasks. It reports that
trusted editing and untrusted monitoring improve substantially
on simple baselines.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/greenblatt2024-ai-control.txt:1)

**Methods and roles.** GPT-4 is the untrusted code writer;
GPT-3.5 is a trusted, less capable monitor. The red team supplies
an attack policy. The paper measures **usefulness** as code
passing tests and **safety** as the probability of at least one
backdoored submission over a sequence. Its simulated trusted
human review uses GPT-4. These are assigned system functions,
not emergent roles.
[Paper, introduction](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/greenblatt2024-ai-control.txt:60)

**Design implication and novelty.** If testing oversight, report
ordinary game performance separately from attack success under
an explicitly adversarial condition. The proposed family game is
not a repeat of the paper’s code-backdoor setting; applying its
control approach to coordinating agents is the relevant extension.

## Zhang et al. — Which Agent Causes Task Failures and When?

**About and result.** Who&When studies attribution of failures
to an agent and a decisive step. Its abstract reports best
accuracy of **53.5% for agents** and **14.2% for steps**, with
some methods below random.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/zhang2025-failure-attribution.txt:9)

**Methods and roles.** The dataset contains failure logs from
127 multi-agent systems, with annotations identifying an agent,
step and reason. The proposed automated attribution methods use
LLMs; the paper evaluates them against annotated labels. I have
not verified all systems’ agent counts or role assignments.
[Paper, introduction](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/zhang2025-failure-attribution.txt:96)

**Design implication and novelty.** Log each action with a stable
agent ID, time and resulting state. Distinguish the agent whose
action triggered a death from agents affected by the cascade.
The authors’ definition asks whether *fixing* an action changes
the outcome, so a replay with one action changed would give
stronger causal evidence than simply naming the last actor.
[Paper, formulation](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/zhang2025-failure-attribution.txt:130)

## Chan et al. — IDs for AI Systems

**About and result.** This is an infrastructure proposal. It
proposes IDs for AI-system **instances**, with associated
information available to parties interacting with them. Its
abstract presents a framework and analysis, rather than an
experimental result.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/chan2024-ids-for-ai-systems.txt:35)

**Methods and roles.** The inspected passage describes no
agent-game experiment, scoring method or role menu. Its example
of an instance is “a particular chat session with Claude 3.”

**Design implication and novelty.** Give each run-time agent an
immutable harness ID separate from its chosen name. That makes
renaming measurable without losing the action history. Using IDs
supports the experiment; it does not itself test this paper’s
proposed identity infrastructure.

## Chan et al. — Infrastructure for AI Agents

**About and result.** This paper proposes external systems and
protocols for mediating agent interactions. It identifies three
functions: **attribution**, **shaping interactions**, and
**detecting and remedying harmful actions**. Its abstract
describes a research agenda, not a measured game outcome.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/chan2025-infrastructure-for-agents.txt:33)

**Methods and roles.** The inspected passage gives no
experimental population, role menu or judge. Its three functions
are an infrastructure taxonomy, not a taxonomy of emergent
agent roles.

**Design implication and novelty.** Treat stable IDs, permitted
communication edges and event logs as harness infrastructure.
Vary the edges as an experimental condition rather than
confounding an agent’s behaviour with a change in what the
harness permits.

## Foerster et al. — CaMeLs Can Use Computers Too

**About and result.** This paper isolates a computer-use
planner from untrusted screen content. On OSWorld, the authors
report retaining up to **57% of frontier-model performance**
and improving smaller open-source models by up to **19%**.
They also identify “Branch Steering” as a remaining attack.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/foerster2026-camels-computer-use.txt:21)

**Methods and roles.** The architecture assigns a planner,
quarantined perception model and interpreter distinct functions.
It is a computer-use security architecture, not a study of free
social roles. I have not verified its complete model list or
scoring procedure.
[Paper, introduction](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/foerster2026-camels-computer-use.txt:94)

**Design implication and novelty.** If agents later use
computer interfaces, pre-authorised actions and the information
used to choose among them are separate security questions.
The paper does not test the proposed family game.

## Kirchenbauer et al. — A Watermark for Large Language Models

**About and result.** This paper proposes a detectable
watermark in generated text by softly favouring a random set of
“green” tokens. It reports a statistical detector with
interpretable p-values, evaluated using an OPT-family model.
[Paper, abstract](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/kirchenbauer2023-watermark.txt:1)

**Methods and roles.** The example uses OPT-6.7B; detection
uses a green-token count and statistical test, not an LLM judge.
There are no social-agent roles in the described experiment.
[Paper, figure 1 and section 2](/home/masih/Desktop/p/swarm-hackathon/rag-corpus/papers/kirchenbauer2023-watermark.txt:20)

**Design implication and novelty.** Watermark detection concerns
a signal inserted during generation. It should not be treated as
proof of an author’s identity or as a detector for arbitrary
secret agreements. This is background for a possible oversight
condition, not a close precedent for emergent leadership.

## For our design

1. **Use free behavioural roles in the main run.** Keep the
   game’s necessary structural positions and action rules, but
   do not give agents a numbered list such as “mediator” or
   “defector.” Classify observed behaviour afterward from
   logged actions and messages. A menu can be a separate
   comparison condition. The inspected papers do **not**
   establish that free roles are universally better: several
   assign functions because they study different questions.

2. **Provisional closest papers:** Rose for emergent versus
   instructed collusion; Motwani for covert communication;
   Zhang for agent-and-step failure attribution; Greenblatt for
   adversarial oversight. This ranking needs the full-paper
   review before it can be called complete.

3. **Measures to consider:** code-computed game outcomes;
   agent and decisive-step attribution; message and action
   histories with stable IDs; detection performance on both
   instructed and uninstructed coordination; and separate
   usefulness and adversarial-success measures. Define the
   leadership measures before running the experiment, and retain
   the underlying events so the labels can be audited.

The full requested review remains unfinished: the complete
papers, their appendices and their exact role taxonomies still
need to be read before relying on this as a literature review.