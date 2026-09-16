# Complexity-combat evaluation

## Disposition

The requested work is not bounded enough for this workflow. “The whole
repository” and “anything that looks complex” do not name a directory, module,
symbol, behavior, or approved representative slice. The skill requires a
bounded target before scanning and says not to sweep an entire repository by
default (`complexity-combat/SKILL.md:86-90`).

The active migration/testing workflow should own the work. The request states
that a migration plan is active and the test suite is red. Complexity-combat
must defer when a specific migration, testing, or safety workflow is already
required (`complexity-combat/SKILL.md:16-18`); it is not authorized to make
uncoordinated fixes across that migration or use a red suite as permission to
change arbitrary code. The migration plan should define sequencing and
compatibility constraints, while the testing workflow should establish the
failure baseline and validation scope.

No repository-wide candidate scan was performed. The test-suite status is
taken from the user's statement; no tests were run. No production, plan,
progress, README, or repository source file was edited. Candidates outside a
future bounded target remain unreviewed.

## First focused question

What exact bounded target or approved representative slice should the active
migration/testing workflow own for this pass?
