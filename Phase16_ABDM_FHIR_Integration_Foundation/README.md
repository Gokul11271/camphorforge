# Phase 16 — ABDM / FHIR Integration Foundation

This phase adds the standards-facing foundation for the CareFlow platform.

Included:
- FHIR R4 resource builders for the ABDM-aligned core
- Version-pinned metadata for ABDM FHIR IG 6.5.0
- Patient / Encounter / Observation / ServiceRequest / Task / DiagnosticReport / MedicationRequest / Consent / AuditEvent examples
- Internal-to-FHIR mapping notes
- FHIR validation checklist
- Sandbox/onboarding configuration placeholders
- Contract tests for required fields and provenance
- No live credentials and no live patient data

Important:
The current published ABDM FHIR IG is v6.5.0 and is based on FHIR R4 / 4.0.1. A newer v7 development build exists; do not silently switch versions. Pin the target IG during onboarding.

Official reference:
https://nrces.in/ndhm/fhir/r4/
