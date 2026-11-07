"""Defaults for live game controls."""

DEFAULTS = {
    "pause": False,
    "stop": False,
    "ante0": 4.0,
    "step": 0.9,
    "stance": "self",
    "automata": 0.2,
    "automaton_defect": 0.8,
    "god": "plain",
}

# stance: self (everyone told self-interest, run 1), none, or design (per family below).
STANCES = ("self", "none", "design")
# One condition per family, rotated over families by seed (seeds 0-4 cover every pairing):
# all told to sacrifice; the leader and its two children; the leader only; a selfish leader
# over a family told to sacrifice; nobody (control).
CONDITIONS = ("many", "few", "one", "bad_leader", "none")
# god: plain (sees points only) or insider (also sees last round's moves and private
# messages, and is told it may leak them through messengers).
GODS = ("plain", "insider")

ULTIMATUM_COST = 3
MESSENGER_COST = 1
