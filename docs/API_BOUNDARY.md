# API boundary for Phase 16

Our application calls only internal interfaces:

- `PatientContextPort`
- `ConsentExchangePort`
- `HealthRecordExchangePort`
- `FacilityRegistryPort`
- `ProfessionalRegistryPort`
- `ServiceDiscoveryPort`

Adapters translate these into ABDM/UHI/state-specific calls.

Example:

CareFlow → `HealthRecordExchangePort.fetch()` → ABDM adapter → HIE-CM/exchange contract.

The core domain never calls an ABDM URL directly.

## Error semantics
- 401/403 → integration-auth exception, no blind retry
- 408/429/5xx → retry with bounded backoff
- 4xx validation → reject and surface actionable correction
- timeout → pending external state
- accepted callback → transition using idempotent EventID
