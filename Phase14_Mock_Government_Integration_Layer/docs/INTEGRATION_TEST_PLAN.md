# Integration contract test plan

## Happy path

1. ABDM patient lookup succeeds.
2. UHI service search returns eligible providers.
3. UHI appointment confirmation returns an appointment reference.
4. eSanjeevani consultation completes.
5. LIS order is accepted and result returned.
6. EMS accepts transport request.
7. External events advance the same JourneyID.

## Failure tests

### Duplicate
Send the same Idempotency-Key twice. Expected: one side effect, second response `DUPLICATE_IGNORED`.

### Timeout
Simulate adapter timeout. Expected: journey remains pending; no false completion.

### 5xx/service outage
Expected: retry policy + circuit breaker + visible operational exception.

### Callback delay
Expected: journey remains in an explicit pending state until acknowledgement.

### Stale facility data
Expected: capability timestamp is visible and recommendation confidence reduced.

### Auth expiry
Expected: authentication failure is surfaced to integration operations, never retried indefinitely.

### Out-of-order event
Expected: event is retained but impossible journey state transition is rejected and reconciled.

### Partial success
Appointment confirmed but transport fails. Expected: appointment remains valid; transport task remains open.

## Assertions

- No duplicate clinical/financial transaction is created by retries.
- Every external event is attributable to source system and JourneyID.
- Every failure is observable.
- External systems remain sources of truth for their own domain.
