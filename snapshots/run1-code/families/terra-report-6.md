Implemented brief 6. The full test suite passed: **44 tests
and 10 subtests**. An offline game run also confirmed that
automaton pairings and moves are logged without exposing
automaton IDs in player prompts.

Rule readings:

- Each live player gets an independent automaton draw in
  even paired rounds. Remaining players pair with each other.
- The family-pool variant has no partners, so it stays unchanged.
- Cross-family identities remain hidden in observations,
  history and partner messages. Variant rules still apply.
- The handbook’s percentages come from the control defaults;
  live control changes do not rewrite that default statement.

The workspace pointer check reported existing issues, including
missing project orientation files. It did not pass.