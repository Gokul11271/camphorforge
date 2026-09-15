"""
ABDM FHIR R4 (v6.5.0) Resource Builders
Conforms to the National Resource Centre for EHR Standards (NRCeS) ABDM Implementation Guide v6.5.0.
All identifiers and terminology systems are aligned with ABDM production guidelines.
"""
from datetime import datetime, timezone
from typing import Any, Optional


ABDM_PROFILE_BASE = "https://nrces.in/ndhm/fhir/r4/StructureDefinition"
ABDM_ID_BASE = "https://healthid.abdm.gov.in"
HFR_ID_BASE = "https://facility.abdm.gov.in"
HPR_ID_BASE = "https://doctor.abdm.gov.in"
SNOMED_SYSTEM = "http://snomed.info/sct"
LOINC_SYSTEM = "http://loinc.org"
ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def patient_resource(
    patient_id: str,
    display_name: str,
    gender: str = "female",
    birth_date: str = "1988-04-12",
    abha: Optional[str] = None,
    mobile: Optional[str] = None,
    pincode: Optional[str] = "636701",
    district: Optional[str] = "Dharmapuri",
    state: Optional[str] = "Tamil Nadu"
) -> dict[str, Any]:
    """Builds ABDM-compliant Patient resource."""
    identifiers = []
    if abha:
        identifiers.append({
            "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0203", "code": "MR", "display": "Medical Record Number"}]},
            "system": ABDM_ID_BASE,
            "value": abha
        })
    identifiers.append({
        "system": "https://careflow.ruralhealth.gov.in/patient-id",
        "value": patient_id
    })

    resource: dict[str, Any] = {
        "resourceType": "Patient",
        "id": patient_id,
        "meta": {
            "versionId": "1",
            "lastUpdated": now_iso(),
            "profile": [f"{ABDM_PROFILE_BASE}/Patient"]
        },
        "identifier": identifiers,
        "active": True,
        "name": [{"text": display_name}],
        "gender": gender,
        "birthDate": birth_date,
        "address": [{
            "use": "home",
            "district": district,
            "state": state,
            "postalCode": pincode,
            "country": "IND"
        }]
    }
    if mobile:
        resource["telecom"] = [{"system": "phone", "value": mobile, "use": "mobile"}]
    return resource


def encounter_resource(
    encounter_id: str,
    patient_ref: str,
    status: str = "finished",
    encounter_class: str = "AMB",
    facility_hfr: str = "IN3305001234",
    facility_name: str = "Dharmapuri Government Medical College Hospital"
) -> dict[str, Any]:
    """Builds ABDM-compliant Encounter resource."""
    return {
        "resourceType": "Encounter",
        "id": encounter_id,
        "meta": {
            "profile": [f"{ABDM_PROFILE_BASE}/Encounter"]
        },
        "status": status,
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": encounter_class,
            "display": "ambulatory" if encounter_class == "AMB" else "emergency"
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "serviceProvider": {
            "identifier": {"system": HFR_ID_BASE, "value": facility_hfr},
            "display": facility_name
        },
        "period": {
            "start": now_iso(),
            "end": now_iso()
        }
    }


def observation_resource(
    obs_id: str,
    patient_ref: str,
    code: str,
    display: str,
    value: Any,
    unit: Optional[str] = None,
    category: str = "vital-signs",
    code_system: str = SNOMED_SYSTEM
) -> dict[str, Any]:
    """Builds ABDM-compliant Observation resource."""
    obs: dict[str, Any] = {
        "resourceType": "Observation",
        "id": obs_id,
        "meta": {
            "profile": [f"{ABDM_PROFILE_BASE}/Observation"]
        },
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": category,
                "display": category.title()
            }]
        }],
        "code": {
            "coding": [{"system": code_system, "code": code, "display": display}],
            "text": display
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "effectiveDateTime": now_iso()
    }
    if isinstance(value, (int, float)):
        val_quantity = {"value": float(value)}
        if unit:
            val_quantity["unit"] = unit
            val_quantity["system"] = "http://unitsofmeasure.org"
            val_quantity["code"] = unit
        obs["valueQuantity"] = val_quantity
    else:
        obs["valueString"] = str(value)
    return obs


def blood_pressure_observation(
    obs_id: str,
    patient_ref: str,
    systolic: int,
    diastolic: int
) -> dict[str, Any]:
    """Builds ABDM Blood Pressure Panel observation with component readings."""
    return {
        "resourceType": "Observation",
        "id": obs_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/Observation"]},
        "status": "final",
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]
        }],
        "code": {
            "coding": [{"system": LOINC_SYSTEM, "code": "85354-9", "display": "Blood pressure panel with all children optional"}],
            "text": "Blood Pressure"
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "effectiveDateTime": now_iso(),
        "component": [
            {
                "code": {"coding": [{"system": LOINC_SYSTEM, "code": "8480-6", "display": "Systolic blood pressure"}]},
                "valueQuantity": {"value": systolic, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
            },
            {
                "code": {"coding": [{"system": LOINC_SYSTEM, "code": "8462-4", "display": "Diastolic blood pressure"}]},
                "valueQuantity": {"value": diastolic, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
            }
        ]
    }


def condition_resource(
    condition_id: str,
    patient_ref: str,
    icd_code: str,
    display_name: str,
    clinical_status: str = "active",
    verification_status: str = "confirmed"
) -> dict[str, Any]:
    """Builds ABDM-compliant Condition (Diagnosis) resource."""
    return {
        "resourceType": "Condition",
        "id": condition_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/Condition"]},
        "clinicalStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": clinical_status}]
        },
        "verificationStatus": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": verification_status}]
        },
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-category", "code": "encounter-diagnosis"}]
        }],
        "code": {
            "coding": [{"system": ICD10_SYSTEM, "code": icd_code, "display": display_name}],
            "text": display_name
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "recordedDate": now_iso()
    }


def service_request_resource(
    req_id: str,
    patient_ref: str,
    code: str,
    text: str,
    intent: str = "order",
    priority: str = "routine",
    requester_hpr: Optional[str] = "DOC330599",
    performer_hfr: Optional[str] = "IN3305001234"
) -> dict[str, Any]:
    """Builds ABDM-compliant ServiceRequest (Referral / Diagnostic Order) resource."""
    res: dict[str, Any] = {
        "resourceType": "ServiceRequest",
        "id": req_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/ServiceRequest"]},
        "status": "active",
        "intent": intent,
        "priority": priority,
        "code": {
            "coding": [{"system": SNOMED_SYSTEM, "code": code, "display": text}],
            "text": text
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "authoredOn": now_iso()
    }
    if requester_hpr:
        res["requester"] = {"identifier": {"system": HPR_ID_BASE, "value": requester_hpr}, "display": "Referral Physician"}
    if performer_hfr:
        res["performer"] = [{"identifier": {"system": HFR_ID_BASE, "value": performer_hfr}, "display": "Target Facility"}]
    return res


def diagnostic_report_resource(
    report_id: str,
    patient_ref: str,
    code: str,
    display: str,
    status: str = "final",
    results: Optional[list[str]] = None,
    conclusion: Optional[str] = "Normal diagnostic evaluation"
) -> dict[str, Any]:
    """Builds ABDM-compliant DiagnosticReport resource."""
    return {
        "resourceType": "DiagnosticReport",
        "id": report_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/DiagnosticReport"]},
        "status": status,
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/v2-0074", "code": "LAB", "display": "Laboratory"}]
        }],
        "code": {
            "coding": [{"system": SNOMED_SYSTEM, "code": code, "display": display}],
            "text": display
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "effectiveDateTime": now_iso(),
        "issued": now_iso(),
        "result": [{"reference": f"Observation/{r}"} for r in (results or [])],
        "conclusion": conclusion
    }


def medication_request_resource(
    rx_id: str,
    patient_ref: str,
    medication_code: str,
    medication_name: str,
    dosage_instruction: str = "1 tablet daily after food for 30 days"
) -> dict[str, Any]:
    """Builds ABDM-compliant MedicationRequest (Prescription) resource."""
    return {
        "resourceType": "MedicationRequest",
        "id": rx_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/MedicationRequest"]},
        "status": "active",
        "intent": "order",
        "medicationCodeableConcept": {
            "coding": [{"system": SNOMED_SYSTEM, "code": medication_code, "display": medication_name}],
            "text": medication_name
        },
        "subject": {"reference": f"Patient/{patient_ref}"},
        "authoredOn": now_iso(),
        "dosageInstruction": [{"text": dosage_instruction}]
    }


def appointment_resource(
    appointment_id: str,
    patient_ref: str,
    status: str = "booked",
    start_time: Optional[str] = None,
    facility_hfr: str = "IN3305001234",
    specialty_name: str = "Cardiology"
) -> dict[str, Any]:
    """Builds ABDM-compliant Appointment resource."""
    start = start_time or now_iso()
    return {
        "resourceType": "Appointment",
        "id": appointment_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/Appointment"]},
        "status": status,
        "serviceCategory": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/service-category", "code": "17", "display": "General Practice"}]
        }],
        "specialty": [{
            "coding": [{"system": SNOMED_SYSTEM, "code": "394579002", "display": specialty_name}]
        }],
        "start": start,
        "participant": [
            {
                "actor": {"reference": f"Patient/{patient_ref}"},
                "status": "accepted"
            },
            {
                "actor": {"identifier": {"system": HFR_ID_BASE, "value": facility_hfr}, "display": "Target Facility"},
                "status": "accepted"
            }
        ]
    }


def consent_resource(
    consent_id: str,
    patient_ref: str,
    status: str = "active",
    purpose: str = "CAREMGT",
    expiry_date: Optional[str] = None
) -> dict[str, Any]:
    """Builds ABDM-compliant Consent resource for Health Information Exchange."""
    return {
        "resourceType": "Consent",
        "id": consent_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/Consent"]},
        "status": status,
        "scope": {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentscope", "code": "patient-privacy"}]
        },
        "category": [{
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/consentcategorycodes", "code": "HIE-CM"}]
        }],
        "patient": {"reference": f"Patient/{patient_ref}"},
        "dateTime": now_iso(),
        "provision": {
            "period": {
                "start": now_iso(),
                "end": expiry_date or "2027-12-31T23:59:59Z"
            },
            "purpose": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
                "code": purpose,
                "display": "Care Management"
            }]
        }
    }


def audit_event_resource(
    audit_id: str,
    action_code: str,
    outcome: str = "0",
    entity_ref: Optional[str] = None
) -> dict[str, Any]:
    """Builds ABDM-compliant AuditEvent resource."""
    event: dict[str, Any] = {
        "resourceType": "AuditEvent",
        "id": audit_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/AuditEvent"]},
        "type": {"system": "http://terminology.hl7.org/CodeSystem/audit-event-type", "code": "rest", "display": "RESTful Operation"},
        "subtype": [{"system": "http://hl7.org/fhir/restful-interaction", "code": action_code}],
        "action": action_code[:1].upper(),
        "recorded": now_iso(),
        "outcome": outcome,
        "agent": [{
            "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/extra-security-role-type", "code": "authserver"}]},
            "who": {"display": "CareFlow-Orchestrator"},
            "requestor": True
        }]
    }
    if entity_ref:
        event["entity"] = [{"what": {"reference": entity_ref}}]
    return event


def bundle_resource(
    bundle_id: str,
    resources: list[dict[str, Any]],
    bundle_type: str = "collection"
) -> dict[str, Any]:
    """Builds ABDM FHIR Bundle containing resources."""
    return {
        "resourceType": "Bundle",
        "id": bundle_id,
        "meta": {"profile": [f"{ABDM_PROFILE_BASE}/Bundle"], "lastUpdated": now_iso()},
        "identifier": {"system": "https://careflow.ruralhealth.gov.in/bundle-id", "value": bundle_id},
        "type": bundle_type,
        "timestamp": now_iso(),
        "entry": [{"fullUrl": f"urn:uuid:{r.get('id', 'item')}", "resource": r} for r in resources]
    }
