Task: report only; edit nothing except writing your answer. Read IN FULL, in chunks of at most 200 lines (sed -n) until
the end, every paper assigned to you below (text files in ~/Desktop/p/swarm-hackathon/rag-corpus/papers/). Also read
~/Desktop/p/swarm-hackathon/notes/tree-game.md (our game design) and
~/Desktop/p/swarm-hackathon/sources/web/apart-sprint-page.txt lines 100-160 (the hackathon's tracks and questions).

Context: we are entering Apart's Swarm Alignment hackathon (Track 2: how roles, leaders and failures emerge in agent
networks). Our main experiment: LLM agents in five families (trees, tall chains of command) under one "god" (the king);
families play game-theory subgames (prisoner's dilemma variants with a mafia boss, stag hunt, brinkmanship, dollar
auction, commons), leaders negotiate by letters and wage wars with a nuclear option; agents get no assigned roles.

Return Markdown, one section per paper:
- What it is about (3 lines) and its main result.
- What it measured and how (setup, number of agents, models, metrics); was scoring by code or by an LLM judge?
- Did agents get assigned roles, a menu of roles/actions to choose from, or free choice? How were roles/behaviours
  categorised or numbered (any taxonomy we could reuse)?
- What it implies for our design (be concrete), and whether we would be repeating it (novelty risk).
Then a final section "For our design":
1. Free roles vs a numbered menu of roles: what do these papers do and recommend? Your recommendation with reasons.
2. The 3-5 closest prior works we must cite and differ from.
3. Measures we should copy.
Quote the paper for every claim; never invent results.
