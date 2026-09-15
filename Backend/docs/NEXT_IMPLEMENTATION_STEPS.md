# Next implementation steps

1. Add JPA entities/repositories for the SQL schema or move schema into Flyway V1/V2 migrations.
2. Add service layer with transactional transition methods.
3. Implement referral endpoint + state transition + event/audit/outbox writes.
4. Implement facility matching as a pure deterministic domain service first.
5. Add UHI adapter mock and contract tests.
6. Add eSanjeevani adapter mock and consultation outcome mapping.
7. Add LIS/LMIS/EMS adapters behind the same interface.
8. Add authentication/authorization and facility-scoped RBAC.
9. Add OpenTelemetry, metrics and structured logs.
10. Add integration tests for outage, retry, duplicate, out-of-order and stale-data cases.
11. Add FHIR validation and ABDM-specific mapper package.
12. Replace mock adapters only after official onboarding and security approval.
