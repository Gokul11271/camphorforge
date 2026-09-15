# Phase 13 — Build Notes

The vertical slice proves the core orchestration loop with synthetic data:

1. Seed an NCD patient and a referral-required journey.
2. View the journey timeline in the browser.
3. Accept the referral.
4. Search facilities using required capabilities.
5. Select a facility and create an appointment reference.
6. Refresh the journey and observe the state transition.

Future work: real FHIR/ABDM mapping, UHI, eSanjeevani, state adapters, auth/RBAC, PostgreSQL HA, event bus/outbox worker, VAPT, offline sync and clinical safety validation.
