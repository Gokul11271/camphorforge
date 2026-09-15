from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Literal

class SearchIntent(BaseModel):
    service_type: str
    specialty: str | None = None
    city: str | None = None
    language: str | None = None
    date: str | None = None

class UhiSearchRequest(BaseModel):
    transaction_id: str
    intent: SearchIntent

class AppointmentRequest(BaseModel):
    provider_ref: str
    patient_ref: str
    slot_start: datetime

class ConsultationRequest(BaseModel):
    patient_ref: str
    reason: str
    provider_ref: str | None = None

class LabOrder(BaseModel):
    order_id: str
    patient_ref: str
    test_code: str

class TransportRequest(BaseModel):
    referral_id: str
    pickup: str
    destination: str
    urgency: str = "ROUTINE"

class ExternalEvent(BaseModel):
    event_id: str
    source_system: str
    event_type: str
    journey_id: str
    occurred_at: datetime
    payload: dict[str, Any] = Field(default_factory=dict)
