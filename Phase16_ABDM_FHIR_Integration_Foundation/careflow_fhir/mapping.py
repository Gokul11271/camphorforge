# Internal care-orchestration → FHIR mapping guide

MAPPING = {
    "PatientRef": "Patient",
    "CareJourney": "CarePlan/Encounter context (the orchestration object itself remains internal)",
    "ClinicalObservation": "Observation",
    "Referral": "ServiceRequest + Task",
    "Appointment": "Appointment",
    "DiagnosticOrder": "ServiceRequest",
    "DiagnosticResult": "DiagnosticReport + Observation",
    "MedicationPlan": "MedicationRequest / MedicationStatement",
    "ConsentContext": "Consent",
    "AuditTrail": "AuditEvent + Provenance",
    "CommunicationTask": "CommunicationRequest",
}

RULES = [
    "Do not use a CareJourney identifier as a substitute for ABHA.",
    "Preserve the source-system identifier and provenance for external records.",
    "Do not manufacture a national facility/professional identifier locally.",
    "Use profile-specific coding/value sets from the pinned ABDM IG package.",
    "Validate resources before sending them to an external exchange.",
]
