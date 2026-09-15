"""
ABDM FHIR R4 (v6.5.0) Conformance & Profile Validator
Validates resource structure, mandatory elements, coding systems, and ABDM IG 6.5.0 profile URI declarations.
"""
from typing import Any


ABDM_PROFILE_BASE = "https://nrces.in/ndhm/fhir/r4/StructureDefinition"

REQUIRED_PROFILES = {
    "Patient": f"{ABDM_PROFILE_BASE}/Patient",
    "Encounter": f"{ABDM_PROFILE_BASE}/Encounter",
    "Observation": f"{ABDM_PROFILE_BASE}/Observation",
    "Condition": f"{ABDM_PROFILE_BASE}/Condition",
    "ServiceRequest": f"{ABDM_PROFILE_BASE}/ServiceRequest",
    "DiagnosticReport": f"{ABDM_PROFILE_BASE}/DiagnosticReport",
    "MedicationRequest": f"{ABDM_PROFILE_BASE}/MedicationRequest",
    "Appointment": f"{ABDM_PROFILE_BASE}/Appointment",
    "Consent": f"{ABDM_PROFILE_BASE}/Consent",
    "AuditEvent": f"{ABDM_PROFILE_BASE}/AuditEvent",
    "Bundle": f"{ABDM_PROFILE_BASE}/Bundle"
}

MANDATORY_FIELDS = {
    "Patient": ["id", "resourceType", "name", "identifier"],
    "Encounter": ["id", "resourceType", "status", "class", "subject"],
    "Observation": ["id", "resourceType", "status", "code", "subject"],
    "Condition": ["id", "resourceType", "code", "subject", "clinicalStatus"],
    "ServiceRequest": ["id", "resourceType", "status", "intent", "code", "subject"],
    "DiagnosticReport": ["id", "resourceType", "status", "code", "subject"],
    "MedicationRequest": ["id", "resourceType", "status", "intent", "subject", "medicationCodeableConcept"],
    "Appointment": ["id", "resourceType", "status", "participant"],
    "Consent": ["id", "resourceType", "status", "scope", "patient", "dateTime"],
    "AuditEvent": ["id", "resourceType", "type", "action", "recorded", "agent"],
    "Bundle": ["id", "resourceType", "type", "entry"]
}


class ConformanceReport:
    def __init__(self, valid: bool, resource_type: str, resource_id: str, errors: list[str], warnings: list[str]):
        self.valid = valid
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.errors = errors
        self.warnings = warnings

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "resourceType": self.resource_type,
            "id": self.resource_id,
            "errors": self.errors,
            "warnings": self.warnings,
            "status": "PASSED" if self.valid else "QUARANTINED"
        }


def validate_resource(resource: dict[str, Any]) -> ConformanceReport:
    """Performs ABDM IG 6.5.0 conformance validation on a single FHIR resource."""
    errors = []
    warnings = []

    res_type = resource.get("resourceType")
    res_id = resource.get("id", "UNKNOWN")

    if not res_type:
        return ConformanceReport(False, "UNKNOWN", res_id, ["Missing required field: resourceType"], [])

    # 1. Check mandatory fields
    required_fields = MANDATORY_FIELDS.get(res_type, ["id", "resourceType"])
    for field in required_fields:
        if field not in resource:
            errors.append(f"Mandatory element missing: '{field}' for {res_type}")

    # 2. Check meta.profile declaration
    meta = resource.get("meta", {})
    profiles = meta.get("profile", [])
    expected_profile = REQUIRED_PROFILES.get(res_type)
    if expected_profile:
        if not profiles:
            warnings.append(f"Resource does not declare meta.profile; expected '{expected_profile}'")
        elif expected_profile not in profiles:
            warnings.append(f"Profile mismatch: got {profiles}, expected '{expected_profile}'")

    # 3. Resource specific checks
    if res_type == "Patient":
        identifiers = resource.get("identifier", [])
        if not any(i.get("system") == "https://healthid.abdm.gov.in" for i in identifiers):
            warnings.append("Patient does not include an official ABDM Health ID / ABHA identifier")

    elif res_type == "Observation":
        code_obj = resource.get("code", {})
        codings = code_obj.get("coding", [])
        if not codings:
            errors.append("Observation.code must contain at least one coding entry")
        valid_systems = {"http://snomed.info/sct", "http://loinc.org", "http://unitsofmeasure.org"}
        for c in codings:
            sys = c.get("system")
            if sys and sys not in valid_systems and not sys.startswith("https://nrces.in"):
                warnings.append(f"Non-standard terminology system in Observation.code: {sys}")

    elif res_type == "Consent":
        if resource.get("status") not in {"draft", "proposed", "active", "rejected", "inactive", "entered-in-error"}:
            errors.append(f"Invalid Consent.status value: '{resource.get('status')}'")

    valid = len(errors) == 0
    return ConformanceReport(valid, res_type, res_id, errors, warnings)


def validate_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    """Validates an entire FHIR Bundle and all nested entries."""
    bundle_report = validate_resource(bundle)
    entries = bundle.get("entry", [])
    entry_reports = []
    all_valid = bundle_report.valid

    for idx, entry in enumerate(entries):
        res = entry.get("resource")
        if not res:
            all_valid = False
            entry_reports.append({"entry_index": idx, "valid": False, "errors": ["Entry missing 'resource' object"]})
            continue
        rep = validate_resource(res)
        if not rep.valid:
            all_valid = False
        entry_reports.append({"entry_index": idx, **rep.to_dict()})

    return {
        "valid": all_valid,
        "bundle_id": bundle.get("id"),
        "total_entries": len(entries),
        "bundle_report": bundle_report.to_dict(),
        "entry_reports": entry_reports,
        "action": "ACCEPTED" if all_valid else "QUARANTINED"
    }
