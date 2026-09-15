# Traceability matrix

| CareFlow capability | FHIR representation | External authority |
|---|---|---|
| Patient identity | Patient | ABDM/ABHA |
| Clinical encounter | Encounter | Provider/EHR |
| Measurement | Observation | Clinical system |
| Referral/diagnostic request | ServiceRequest | Requesting clinician/system |
| Operational work | Task | CareFlow |
| Result/report | DiagnosticReport | LIS/EHR |
| Prescription | MedicationRequest | Prescribing clinician/system |
| Consent | Consent | ABDM consent context / governing consent mechanism |
| Audit | AuditEvent / Provenance | CareFlow + system audit |
