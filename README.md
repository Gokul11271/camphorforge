# Phase 15 — End-to-End System Validation

This package is a self-contained validation harness for the CareFlow architecture.

It validates the orchestration logic without connecting to live government systems.

Validated scenarios:
1. Happy-path NCD referral journey
2. Duplicate external event
3. External timeout / pending state
4. Referral rejection + re-routing
5. Diagnostic delay / SLA breach
6. Partial success (appointment confirmed, transport pending)
7. Offline event replay
8. Out-of-order event rejection
9. Audit/provenance completeness
10. Care-journey closure gate

Run:

    python tests/run_tests.py

Expected result: PASS for all scenarios.

The implementation is intentionally lightweight so it can run without installing third-party packages. It is a contract/invariant harness, not a production server.
