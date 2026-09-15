# Sandbox and onboarding checklist

1. Register the organization/facility with the relevant ABDM onboarding path.
2. Obtain sandbox credentials and environment URLs from official onboarding.
3. Register/verify the required HFR and professional/facility context.
4. Implement discovery/linking and consent flows required for the selected HIP/HIU role.
5. Validate FHIR payloads against the pinned IG version.
6. Run official sandbox test cases.
7. Complete required security testing/certification.
8. Receive production approval before enabling live traffic.

Do not commit secrets to git. Use a secret manager and inject credentials via environment/workload identity.
