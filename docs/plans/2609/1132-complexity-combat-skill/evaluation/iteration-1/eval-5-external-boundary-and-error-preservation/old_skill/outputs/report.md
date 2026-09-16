# Complexity scan: external boundary

| Candidate | Evidence | Problem addressed | Assessment | Impact |
|---|---|---|---|---|
| External-service `NetworkError` handling (fixture lines 5–9) | `client.fetch_profile(user_id)` is called through the supplied client, and `client.NetworkError` is caught, logged, and converted to `None` ([`external_boundary.py:5-9`](../../../../../evals/fixtures/external_boundary.py:5)). | Preserve a stable application boundary when the external profile service is unavailable, while retaining an operational warning. | Justified on the available evidence. The client is explicitly an external service, and the evaluation contract identifies this error behavior as observable. There is no evidence that `NetworkError` cannot occur or that preserving the failure boundary is unnecessary. | Medium |
| Null payload check (fixture lines 11–12) | The result of the external call is checked for `None` before `normalize_profile(payload)` ([`external_boundary.py:6,11-14`](../../../../../evals/fixtures/external_boundary.py:6)). | Preserve the external service's null-payload behavior and avoid normalizing an absent profile. | Justified on the available evidence. The evaluation contract explicitly says null payload behavior is part of the observable boundary, and no contrary non-null contract is present. This should not be called accidental complexity. | Low |

## First decision — stop here

### Candidate 1: external-service `NetworkError` handling

This code addresses: “Convert an external profile-service failure into a logged, stable `None` result while preserving the service boundary.”

Is this a real problem for your project?

- **Yes** — keep the exception handling.
- **No** — simplify or remove it.
- **Maybe, but overblown** — simplify with care.

No edit or recommendation about the next candidate will be made until this decision is answered.
