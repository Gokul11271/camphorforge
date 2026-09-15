from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Header
from .models import *
from .state import STATE

app = FastAPI(title="CareFlow Mock Integration Gateway", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "UP", "mode": "MOCK_ONLY"}

@app.get("/abdm/patient/{patient_ref}")
def abdm_patient(patient_ref: str):
    if patient_ref != "DEMO-ABHA-281":
        raise HTTPException(404, "Patient reference not found in demo")
    return {
        "resourceType": "Patient",
        "id": patient_ref,
        "identifier": [{"system": "https://healthid.abdm.gov.in", "value": patient_ref}],
        "name": [{"text": "Meenakshi R."}],
        "gender": "female"
    }

@app.post("/uhi/search")
def uhi_search(req: UhiSearchRequest):
    matches = []
    for p in STATE["uhI"]["providers"]:
        if req.intent.service_type and p["service"] != req.intent.service_type:
            continue
        if req.intent.specialty and p["specialty"] != req.intent.specialty:
            continue
        if req.intent.city and p["city"].lower() != req.intent.city.lower():
            continue
        if req.intent.language and p["language"] != req.intent.language:
            continue
        if p["availability"] in {"AVAILABLE","LIMITED"}:
            matches.append(p)
    return {"transaction_id": req.transaction_id, "providers": matches}

@app.post("/uhi/appointments")
def uhi_appointment(req: AppointmentRequest, idempotency_key: str | None = Header(default=None)):
    key = idempotency_key or f"{req.patient_ref}:{req.provider_ref}:{req.slot_start.isoformat()}"
    existing = STATE["uhI"]["appointments"].get(key)
    if existing:
        return {"status": "DUPLICATE_IGNORED", "appointment": existing}
    appt = {
        "appointment_ref": f"UHI-APPT-{len(STATE['uhI']['appointments'])+1:04d}",
        "provider_ref": req.provider_ref,
        "patient_ref": req.patient_ref,
        "slot_start": req.slot_start.isoformat(),
        "status": "CONFIRMED"
    }
    STATE["uhI"]["appointments"][key] = appt
    return {"status": "CONFIRMED", "appointment": appt}

@app.post("/esanjeevani/consultations")
def consultation(req: ConsultationRequest):
    cid=f"ESANJ-DEMO-{len(STATE['consultations'])+1:04d}"
    record={
        "consultation_id": cid,
        "patient_ref": req.patient_ref,
        "provider_ref": req.provider_ref or "demo-specialist-001",
        "status": "COMPLETED",
        "clinical_outcome_ref": f"OUTCOME-{cid}",
        "referral_recommended": True
    }
    STATE["consultations"][cid]=record
    return record

@app.post("/lis/orders")
def lab_order(req: LabOrder):
    STATE["labs"][req.order_id]={"order_id":req.order_id,"patient_ref":req.patient_ref,"test_code":req.test_code,"status":"IN_PROGRESS"}
    return STATE["labs"][req.order_id]

@app.post("/lis/orders/{order_id}/result")
def lab_result(order_id: str):
    if order_id not in STATE["labs"]:
        raise HTTPException(404, "Lab order not found")
    record={
        "report_id": f"LIS-{order_id}",
        "order_id": order_id,
        "status": "FINAL",
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "tests": [{"code": STATE["labs"][order_id]["test_code"], "value": "9.4", "unit": "%"}]
    }
    STATE["labs"][order_id].update(record)
    return record

@app.post("/ems/transport")
def ems_transport(req: TransportRequest, idempotency_key: str | None = Header(default=None)):
    key=idempotency_key or req.referral_id
    if key in STATE["ems"]:
        return {"status":"DUPLICATE_IGNORED","transport":STATE["ems"][key]}
    record={
        "transport_id":f"EMS-DEMO-{len(STATE['ems'])+1:04d}",
        "status":"DISPATCHED",
        "mode":"BLS",
        "pickup":req.pickup,
        "destination":req.destination,
        "eta_minutes":42,
        "referral_id":req.referral_id
    }
    STATE["ems"][key]=record
    return record

@app.post("/events")
def receive_event(req: ExternalEvent, idempotency_key: str | None = Header(default=None)):
    key = idempotency_key or req.event_id
    if any(e["dedupe_key"] == key for e in STATE["events"]):
        return {"status":"DUPLICATE_IGNORED"}
    STATE["events"].append({"dedupe_key": key, **req.model_dump(mode="json")})
    return {"status":"ACCEPTED","event_id":req.event_id}
