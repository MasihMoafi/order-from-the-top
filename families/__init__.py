"""Initialize Five Families and expose game helpers used by arena imports.

Importing this package attaches the shared game.game exports to game before
arena.arena loads, so both import paths use the same Budget class.
"""

import game as _game
from game.game import BASE, MODEL, Budget, append_lines

_game.BASE, _game.MODEL, _game.Budget, _game.append_lines = BASE, MODEL, Budget, append_lines
