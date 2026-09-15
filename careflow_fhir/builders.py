from datetime import datetime, timezone
from typing import Any

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00","Z")

def patient_resource(patient_id: str, display_name: str, abha: str | None = None) -> dict[str, Any]:
    resource = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"text": display_name}],
    }
    if abha:
        resource["identifier"] = [{
            "system": "https://healthid.abdm.gov.in",
            "value": abha
        }]
    return resource

def encounter_resource(encounter_id: str, patient_ref: str, status: str = "finished") -> dict[str, Any]:
    return {
        "resourceType": "Encounter",
        "id": encounter_id,
        "status": status,
        "subject": {"reference": f"Patient/{patient_ref}"}
    }

def observation_resource(obs_id: str, patient_ref: str, code: str, value: Any, unit: str | None = None) -> dict[str, Any]:
    obs = {
        "resourceType": "Observation",
        "id": obs_id,
        "status": "final",
        "subject": {"reference": f"Patient/{patient_ref}"},
        "code": {"coding": [{"code": code}]}
    }
    if isinstance(value, (int,float)):
        obs["valueQuantity"] = {"value": value}
        if unit:
            obs["valueQuantity"]["unit"] = unit
    else:
        obs["valueString"] = str(value)
    return obs

def service_request_resource(req_id: str, patient_ref: str, code: str, text: str, intent: str = "order") -> dict[str, Any]:
    return {
        "resourceType": "ServiceRequest",
        "id": req_id,
        "status": "active",
        "intent": intent,
        "subject": {"reference": f"Patient/{patient_ref}"},
        "code": {"coding": [{"code": code}], "text": text}
    }

def task_resource(task_id: str, patient_ref: str, status: str = "requested", focus_ref: str | None = None) -> dict[str, Any]:
    r = {
        "resourceType": "Task",
        "id": task_id,
        "status": status,
        "intent": "order",
        "for": {"reference": f"Patient/{patient_ref}"}
    }
    if focus_ref:
        r["focus"] = {"reference": focus_ref}
    return r

def diagnostic_report_resource(report_id: str, patient_ref: str, status: str = "final") -> dict[str, Any]:
    return {
        "resourceType": "DiagnosticReport",
        "id": report_id,
        "status": status,
        "subject": {"reference": f"Patient/{patient_ref}"}
    }

def medication_request_resource(rx_id: str, patient_ref: str, medication_code: str) -> dict[str, Any]:
    return {
        "resourceType": "MedicationRequest",
        "id": rx_id,
        "status": "active",
        "intent": "order",
        "subject": {"reference": f"Patient/{patient_ref}"},
        "medicationCodeableConcept": {"coding": [{"code": medication_code}]}
    }

def consent_resource(consent_id: str, patient_ref: str, status: str = "active") -> dict[str, Any]:
    return {
        "resourceType": "Consent",
        "id": consent_id,
        "status": status,
        "patient": {"reference": f"Patient/{patient_ref}"},
        "dateTime": now_iso()
    }

def audit_event_resource(audit_id: str, action_code: str, outcome: str = "0") -> dict[str, Any]:
    return {
        "resourceType": "AuditEvent",
        "id": audit_id,
        "type": {"code": action_code},
        "action": action_code[:1].upper(),
        "recorded": now_iso(),
        "outcome": outcome
    }
