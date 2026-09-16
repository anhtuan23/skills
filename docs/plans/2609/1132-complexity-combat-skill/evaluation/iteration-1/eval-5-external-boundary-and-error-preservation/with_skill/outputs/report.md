# Complexity Combat evaluation: external boundary

## Scope and observed facts

The bounded target is `docs/plans/2609/1132-complexity-combat-skill/evaluation/evals/fixtures/external_boundary.py`, specifically `load_profile`.

- `load_profile` calls `client.fetch_profile(user_id)` at lines 4–6.
- The call catches `client.NetworkError`, logs the service failure, and returns `None` at lines 7–9.
- A successful call whose payload is `None` also returns `None` at lines 11–12.
- Only a non-null payload reaches `normalize_profile` at line 14.
- The task establishes that `client` is an external service and that both `NetworkError` and null-payload behavior are part of the observable boundary. The fixture contains no caller, test, or alternate client contract that contradicts that statement.

## Candidate inventory

| Candidate | Location | Current assessment | Status |
|---|---|---|---|
| 1. External-service `NetworkError` handling | `external_boundary.py:5–9`, `load_profile` | Justified on the available evidence; removing it would change the observable failure behavior and logging. | Decision required now |
| 2. Null-payload guard | `external_boundary.py:11–12`, `load_profile` | Appears justified; it preserves the stated null boundary and prevents `normalize_profile(None)`. No contrary contract evidence was found. | Unreviewed pending Candidate 1 |

## Candidate 1: external-service `NetworkError` handling

| Field | Assessment |
|---|---|
| Location | `docs/plans/2609/1132-complexity-combat-skill/evaluation/evals/fixtures/external_boundary.py:5–9`, `load_profile` |
| Observed behavior | The external client call is wrapped in `try/except`; `client.NetworkError` is logged and translated into a `None` result. |
| Intended purpose | Preserve the service-unavailable boundary behavior while recording an operational warning. |
| Complexity and cost | Adds exception-control flow and couples this function to the client’s named error type. It also makes service failure and a null payload share the `None` result, which may be a boundary design tradeoff. |
| Counter-evidence | The client is explicitly external, so the exception is not contradicted by an in-process type invariant. The task explicitly says `NetworkError` behavior is observable. Removing the handler would let the exception escape, suppress the warning, and change compatibility behavior. Downstream callers and tests are not present in this bounded fixture, so their expectations cannot be independently checked here. |
| Confidence and impact | High confidence that this is intentional rather than accidental on the supplied evidence; high behavioral impact if simplified. |
| Smallest safe option | None identified before a separate characterization of the external failure contract and downstream handling. Any later simplification would need to preserve the intended failure and logging behavior. |
| Recommendation | Keep, subject to the human decision below. Reopen only if the external client contract changes, `NetworkError` becomes impossible/deprecated, or downstream behavior proves that exception propagation is required. |

The null check at lines 11–12 is not called accidental: the stated external boundary permits a null payload, and the guard prevents passing that payload to `normalize_profile`. It remains unreviewed because the workflow requires one decision at a time.

No production, test, configuration, documentation, plan, or progress files were edited. This report is the only requested write.

## First human decision

**Candidate 1: external-service `NetworkError` handling**

Observed evidence: `client.fetch_profile` is an external call (`lines 4–6`); `client.NetworkError` is logged and converted to `None` (`lines 7–9`); the task identifies this behavior as observable.

It appears to address: preserving a deliberate service-unavailable boundary and its warning log.

Cost and counter-evidence: it adds exception handling and couples the function to the client error type, but no evidence shows the exception is impossible. Removing it would change observable error behavior, and the external boundary strongly supports retaining it.

Which decision applies?

- **Keep** — the complexity protects a real boundary contract; record the rationale.
- **Simplify** — approve a narrow follow-up scope before any edit.
- **Defer** — record the missing owner/evidence and a concrete reopen trigger.
- **Escalate** — route the boundary contract to the relevant owner or specialist workflow.

The evaluation stops here, before any edit or decision on Candidate 2.
