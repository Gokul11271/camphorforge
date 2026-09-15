# ABDM/FHIR implementation rules

## Version pin
- HL7 FHIR: R4 / 4.0.1
- ABDM FHIR IG: 6.5.0 for the current published baseline
- Package: ndhm.in#6.5.0

A 7.0.0 development build is published under a preview path. It should not replace the pinned release in this codebase without a controlled compatibility review.

## Core resources
The first vertical slice uses:
- Patient
- Encounter
- Observation
- ServiceRequest
- Task
- DiagnosticReport
- MedicationRequest
- Consent
- AuditEvent
- Provenance (where source lineage must be explicit)

## Validation
Use the official IG package and a FHIR validator rather than hand-written validation alone. CI should validate JSON/XML resources against the pinned profiles.

## Terminology
Use the terminology/value-set packages defined by the selected ABDM IG. Do not invent local codes where a standard/code system is required.

## Provenance
Every resource derived from an external programme/service should carry enough source metadata for reconstruction and audit, according to the applicable profile and governance.

## Security
FHIR resources can contain sensitive health information. Never log full resource bodies in ordinary application logs. Use structured access/audit events instead.
