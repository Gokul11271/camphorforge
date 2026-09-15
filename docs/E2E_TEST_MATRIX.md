# End-to-end validation matrix

| Scenario | What is validated | Expected |
|---|---|---|
| Happy path | Full state-machine journey | CLOSED |
| Duplicate event | Idempotent integration | No duplicate side effect |
| Timeout | External dependency failure | Pending, not success |
| Referral rejection | Safe rerouting | Journey remains REFERRAL_REQUIRED |
| Diagnostic delay | Pending dependency | Journey remains open |
| Partial success | Appointment without transport | Open with transport pending |
| Offline replay | Reconnect after offline event | Single event |
| Out-of-order | Invalid state transition | Rejected |
| Audit | Traceability | Audit + source on events |
| Closure gate | No premature closure | Blocked until criteria met |

## Promotion criteria

- 100% automated contract/invariant tests pass.
- No invalid state transition is accepted.
- Duplicate inbound events produce no second side effect.
- External failure never produces a false success.
- Pending external work is visible.
- Every patient-impacting transition has actor/source/timestamp evidence.
- Offline replay is deterministic.
