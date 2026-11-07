"""Five Families deterministic game engine."""

# arena.arena still imports these names from the old top-level game module.
# Load the package first so both it and families use the same game.game module.
import game as _game
from game.game import BASE, MODEL, Budget, append_lines

_game.BASE, _game.MODEL, _game.Budget, _game.append_lines = BASE, MODEL, Budget, append_lines
