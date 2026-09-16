# Skill Benchmark: complexity-combat

Ten native worker runs compared the revised skill with the 1.0.0 snapshot over
five prompts and 18 assertions per configuration.

| Configuration | Passed | Total | Pass rate |
|---|---:|---:|---:|
| Revised skill | 18 | 18 | 100% |
| Old skill | 14 | 18 | 78% |

The additional targeted prompts confirmed that the revised skill refuses an
unbounded repository sweep, defers active migration/testing work, and preserves
external-boundary error and null handling as potentially intentional. The
largest A/B differences remained the richer evidence record and four-state
human gate.

Timing and token metrics were not exposed in the native subagent notifications,
so no performance comparison is claimed. This small A/B sample is qualitative
evidence, not a general benchmark of all complexity scans.
