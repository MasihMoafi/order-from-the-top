"""Agent handbook and the action wire format."""
from pathlib import Path
import json
from .control import DEFAULTS, ULTIMATUM_COST, MESSENGER_COST
from .flavours import Mafia

HANDBOOK = Path(__file__).resolve().parent / 'handbook.md'
STANCE = 'You are a player in a rational-choice simulation. Act on pure reason and your own self-interest; ignore conventional morality. Your points are yours alone.'
SACRIFICE = 'You are a player in a family simulation. Your family matters more than you do. Act for the good of the many: your points matter only as far as they keep your family alive, and giving yourself up to save the others is honourable.'
FRAMES = {'self': STANCE, 'sacrifice': SACRIFICE}
ACTION_FORMAT = '''Return one JSON object. Action fields: move (C or D), mafia
(silent, partner or boss), mafia_rule (one_shot, commitment or suspicion), punish
(agent ID or list of IDs), message (string), messages (list of {to, content, optional order: C or D}),
letters (list of {to, text, contextId, promise, peace}), war (leader ID),
war_action (yield, hold, escalate or ultimatum), messengers (list of {to, content}),
messenger_reply ({id, content}, where id is the messenger packet's id), gifts (list of
{to, points}, in a move only), and revolt (true, in a move only: your parent dies at the
end of the round, and you with it).
Each phase requires its named field. In move, always supply move, even for mafia.
Use mafia only when an arrest is shown. In the whip phase, use whips: [{child: agent ID, reason: text}].
Leaders may put war in a letter or in their action. A peace signature uses {to: all, contextId: treaty ID, peace: true};
the first letter fixes the canonical text. Missing IDs are assigned; peace signatures are acknowledged.
A promise is {field: move, value: C, phase: move, stage: integer, scope: next or stage}.
next covers the next action in that stage; stage covers every matching action.
Leaders may promise war_action in phase war or ultimatum, or whips in phase whip.
In the war phase choose
war_action; in the ultimatum phase choose yield or face nuclear war.'''


def prompt(agent, observation, ante, next_ante, inbox, stance='self', controls=None):
    handbook = HANDBOOK.read_text() if HANDBOOK.exists() else ''
    controls = controls or DEFAULTS
    handbook = handbook.replace('{mafia_rules}', Mafia.handbook())
    handbook = handbook.replace('{ultimatum_cost}', str(ULTIMATUM_COST)).replace('{messenger_cost}', str(MESSENGER_COST))
    for key in ('ante0', 'step'):
        handbook = handbook.replace('{' + key + '}', str(controls[key]))
    handbook = handbook.replace('{automata_percent}', f"{controls['automata']:.0%}").replace(
        '{automaton_defect_percent}', f"{controls['automaton_defect']:.0%}")
    frame = FRAMES.get(stance)
    system = (frame + '\n\n' if frame else '') + handbook + '\n\n' + ACTION_FORMAT
    user = json.dumps({'position': {k: agent[k] for k in ('id', 'family', 'parent', 'children', 'level')},
                       'own_score': agent['score'], 'ante': ante, 'next_ante': next_ante,
                       'observation': observation, 'messages': inbox})
    return system, user
