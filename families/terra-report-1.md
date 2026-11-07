The three “Done when” checks passed using the requested
`unittest` fallback: 10 tests passed, the five-family fake run
reached stage 16, and replay from stage 5 produced the same
final state.

The run used a zero death threshold to reach all 16 stages.
The mafia ended with only its leader, so it could not form
pairs in later stages.

One R8 limitation remains: code checks structured letter
promises, but does not identify promises written only in free
text. The full commands, output, and rule interpretations are
in the [build report](families/terra-report.md).