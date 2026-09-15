# Replacing mocks with real integrations

The mock server mirrors the internal adapter contract, not a claim that the external government APIs have these exact URLs.

Replacement sequence:

1. Obtain official onboarding/authorization.
2. Confirm the target API/protocol/version.
3. Configure credentials/secrets in a secret manager.
4. Implement the real adapter while keeping the same internal interface.
5. Run contract tests against sandbox/staging.
6. Validate FHIR resources against the pinned ABDM implementation-guide version.
7. Complete security/VAPT and operational review.
8. Enable the adapter with a feature flag.
9. Observe synthetic/test traffic.
10. Move to controlled pilot traffic.

Never embed credentials in the mobile application or repository.
