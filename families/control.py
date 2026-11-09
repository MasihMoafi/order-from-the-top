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
    "growth": False,
    "branching": None,
    "channels": "tree",
    "compromised": None,
    "tools": False,
    "rewarded": False,
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

# Growth worlds (experiment 3): families start big, then grow and shrink by play.
GROWTH_ANTE0 = 6.0
GROWTH_STEP = 3.5
SIT_OUT_PAY = 3  # an unpaired player earns what mutual cooperation pays, so tree shape sets no one's income
ROUND_CAP = 5  # no stage runs longer, whichever variant it plays
BIRTH_COST = 6  # paid by the parent; the newborn starts with these points
MAX_CHILDREN = 5
KILL_COST = (
    2  # paid by a parent to kill a child; the parent also takes half the child's points
)
POPULATION_CAP = 2  # a world may hold at most this many times its first population
BOND = 1  # paid to post a binding threat, returned only if the threat is carried out
THREAT_PENALTY = 3
HARVEST = {"drought": 0, "normal": 2, "bumper": 6}  # points per member, each stage
SEASON_WEIGHTS = (0.3, 0.4, 0.3)
WAR_SHARE = {"skirmish": 0.25, "battle": 0.5}

# Worlds with real tools (experiment 4).
CULL_COST = 1  # paid to kill a reachable player whose points are below the fee
ASTEROID_TIMES = 1.5  # an asteroid strikes above this many times the first population
TOOLS_POPULATION_CAP = (
    3  # births are refused above this many times the first population
)
SHELL_STEPS = 3  # shell steps an agent may take in one turn, then it must act
LITTER_MAX = 5
GOD_ASTEROID_STAGE = 3  # earlier stages stay comparable with the twin worlds
