"""
CareFlow Production-Grade Orchestration Engine
Implements 14-state Care Journey, Closed-Loop Referral Lifecycle, Diagnostic SLA Tracking,
Transport Coordination, and Data Freshness Integration.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Optional
import uuid
import hashlib
import json

from freshness import FreshnessClass, FreshnessMetadata, FreshnessEngine, VerificationStatus


class State(str, Enum):
    NEW = "NEW"
    TRIAGED = "TRIAGED"
    CONSULTATION_REQUIRED = "CONSULTATION_REQUIRED"
    CONSULTED = "CONSULTED"
    DIAGNOSTIC_REQUIRED = "DIAGNOSTIC_REQUIRED"
    DIAGNOSTIC_IN_PROGRESS = "DIAGNOSTIC_IN_PROGRESS"
    DIAGNOSTIC_COMPLETED = "DIAGNOSTIC_COMPLETED"
    REFERRAL_REQUIRED = "REFERRAL_REQUIRED"
    REFERRAL_ACCEPTED = "REFERRAL_ACCEPTED"
    APPOINTMENT_CONFIRMED = "APPOINTMENT_CONFIRMED"
    TRANSPORT_CONFIRMED = "TRANSPORT_CONFIRMED"
    PATIENT_ARRIVED = "PATIENT_ARRIVED"
    TREATMENT_COMPLETED = "TREATMENT_COMPLETED"
    MEDICINE_FULFILLED = "MEDICINE_FULFILLED"
    FOLLOW_UP_ACTIVE = "FOLLOW_UP_ACTIVE"
    CLOSED = "CLOSED"


ALLOWED_TRANSITIONS: dict[State, set[State]] = {
    State.NEW: {State.TRIAGED},
    State.TRIAGED: {State.CONSULTATION_REQUIRED, State.CONSULTED},
    State.CONSULTATION_REQUIRED: {State.CONSULTED},
    State.CONSULTED: {State.DIAGNOSTIC_REQUIRED, State.REFERRAL_REQUIRED, State.FOLLOW_UP_ACTIVE},
    State.DIAGNOSTIC_REQUIRED: {State.DIAGNOSTIC_IN_PROGRESS, State.DIAGNOSTIC_COMPLETED},
    State.DIAGNOSTIC_IN_PROGRESS: {State.DIAGNOSTIC_COMPLETED},
    State.DIAGNOSTIC_COMPLETED: {State.REFERRAL_REQUIRED, State.FOLLOW_UP_ACTIVE, State.TREATMENT_COMPLETED},
    State.REFERRAL_REQUIRED: {State.REFERRAL_ACCEPTED, State.REFERRAL_REQUIRED},  # self-loop for re-routing on rejection
    State.REFERRAL_ACCEPTED: {State.APPOINTMENT_CONFIRMED},
    State.APPOINTMENT_CONFIRMED: {State.TRANSPORT_CONFIRMED, State.PATIENT_ARRIVED},
    State.TRANSPORT_CONFIRMED: {State.PATIENT_ARRIVED},
    State.PATIENT_ARRIVED: {State.TREATMENT_COMPLETED},
    State.TREATMENT_COMPLETED: {State.MEDICINE_FULFILLED, State.FOLLOW_UP_ACTIVE},
    State.MEDICINE_FULFILLED: {State.FOLLOW_UP_ACTIVE},
    State.FOLLOW_UP_ACTIVE: {State.CLOSED},
}


@dataclass
class JourneyEvent:
    event_id: str
    event_type: str
    source_system: str
    occurred_at: datetime
    received_at: datetime
    payload: dict[str, Any] = field(default_factory=dict)
    payload_hash: str = ""

    def __post_init__(self):
        if not self.payload_hash:
            raw = json.dumps(self.payload, sort_keys=True, default=str).encode("utf-8")
            self.payload_hash = hashlib.sha256(raw).hexdigest()


@dataclass
class ReferralRecord:
    referral_id: str
    journey_id: str
    source_facility_id: str
    target_facility_id: Optional[str]
    specialty_required: str
    urgency: str  # ROUTINE, URGENT, EMERGENCY
    status: str   # CREATED, ACCEPTED, REJECTED, REROUTED, COMPLETED
    sla_deadline: datetime
    created_at: datetime
    freshness: Optional[FreshnessMetadata] = None
    rejection_reason: Optional[str] = None


@dataclass
class DiagnosticRecord:
    order_id: str
    journey_id: str
    test_code: str
    test_name: str
    facility_id: str
    status: str  # ORDERED, SPECIMEN_COLLECTED, PROCESSING, COMPLETED, DELAYED
    is_critical: bool
    result_ref: Optional[str] = None
    sla_deadline: Optional[datetime] = None
    freshness: Optional[FreshnessMetadata] = None


@dataclass
class MedicineRecord:
    prescription_id: str
    journey_id: str
    medication_code: str
    medication_name: str
    quantity: int
    facility_id: str
    stock_status: str  # AVAILABLE, LOW_STOCK, STOCK_OUT, DISPENSED
    stock_confidence: float
    freshness: Optional[FreshnessMetadata] = None


@dataclass
class TransportRecord:
    transport_id: str
    referral_id: str
    vehicle_id: Optional[str]
    pickup_location: str
    destination: str
    status: str  # REQUESTED, DISPATCHED, IN_TRANSIT, ARRIVED, CANCELLED
    status_source: str  # LIVE_GPS, PERIODIC, EVENT_ONLY, UNAVAILABLE
    last_gps_update: Optional[datetime] = None
    freshness: Optional[FreshnessMetadata] = None


@dataclass
class Journey:
    journey_id: str
    patient_id: str
    pathway: str  # NCD_HYPERTENSION, MATERNAL_ANC, CHILD_IMMUNIZATION, TB_DOTS
    state: State = State.NEW
    events: list[JourneyEvent] = field(default_factory=list)
    audit_trail: list[dict[str, Any]] = field(default_factory=list)
    pending_external: set[str] = field(default_factory=set)
    referral: Optional[ReferralRecord] = None
    diagnostics: list[DiagnosticRecord] = field(default_factory=list)
    medicines: list[MedicineRecord] = field(default_factory=list)
    transport: Optional[TransportRecord] = None
    opened_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None


class Engine:
    """Production-grade Care Orchestration Engine managing the 14-state journey with freshness."""

    def __init__(self):
        self.journeys: dict[str, Journey] = {}
        self.seen_events: set[tuple[str, str]] = set()  # (source_system, event_id)
        self.freshness_engine = FreshnessEngine()

    def create(self, journey_id: str, patient_id: str = "PAT-001", pathway: str = "NCD_HYPERTENSION") -> Journey:
        j = Journey(journey_id=journey_id, patient_id=patient_id, pathway=pathway)
        self.journeys[journey_id] = j
        self.audit(journey_id, "CREATE_JOURNEY", f"CareJourney:{pathway}")
        return j

    def audit(self, journey_id: str, action: str, resource: str, metadata: Optional[dict[str, Any]] = None) -> None:
        entry = {
            "audit_id": str(uuid.uuid4()),
            "journey_id": journey_id,
            "action": action,
            "resource": resource,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {}
        }
        if journey_id in self.journeys:
            self.journeys[journey_id].audit_trail.append(entry)

    def transition(
        self,
        journey_id: str,
        to_state: State | str,
        event_id: str,
        source_system: str,
        payload: Optional[dict[str, Any]] = None
    ) -> str:
        j = self.journeys.get(journey_id)
        if not j:
            raise KeyError(f"Journey {journey_id} not found")

        if not isinstance(to_state, State):
            to_state = State(to_state)

        # Invariant check
        if to_state not in ALLOWED_TRANSITIONS.get(j.state, set()):
            raise ValueError(f"Invalid care journey transition: {j.state.value} -> {to_state.value}")

        # Idempotency check per journey
        if any(e.event_id == event_id for e in j.events):
            return "DUPLICATE_IGNORED"

        now = datetime.now(timezone.utc)
        evt = JourneyEvent(
            event_id=event_id,
            event_type=f"JourneyStateChanged:{to_state.value}",
            source_system=source_system,
            occurred_at=now,
            received_at=now,
            payload=payload or {}
        )
        j.state = to_state
        j.events.append(evt)
        self.audit(journey_id, "STATE_TRANSITION", f"{j.state.value}", {"event_id": event_id, "source": source_system})
        return "APPLIED"

    def ingest_external(
        self,
        journey_id: str,
        event_id: str,
        event_type: str,
        source_system: str,
        payload: Optional[dict[str, Any]] = None,
        freshness_class: FreshnessClass = FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
    ) -> str:
        key = (source_system, event_id)
        if key in self.seen_events:
            return "DUPLICATE_IGNORED"
        self.seen_events.add(key)

        j = self.journeys.get(journey_id)
        if not j:
            raise KeyError(f"Journey {journey_id} not found")

        now = datetime.now(timezone.utc)
        evt = JourneyEvent(
            event_id=event_id,
            event_type=event_type,
            source_system=source_system,
            occurred_at=now,
            received_at=now,
            payload=payload or {}
        )
        j.events.append(evt)

        # Register freshness metadata
        meta = FreshnessMetadata.create(
            source_system=source_system,
            source_record_id=event_id,
            data_type=event_type,
            freshness_class=freshness_class
        )
        self.freshness_engine.register(f"{journey_id}:{event_type}:{event_id}", meta)

        self.audit(journey_id, "EXTERNAL_EVENT", event_type, {"source": source_system, "freshness": meta.get_ui_badge()})
        return "ACCEPTED"

    def handle_referral_rejection(self, journey_id: str, reason: str, alternative_facility: str) -> None:
        """Handles referral rejection and reroutes without corrupting state machine."""
        j = self.journeys[journey_id]
        if j.referral:
            j.referral.status = "REROUTED"
            j.referral.rejection_reason = reason
            j.referral.target_facility_id = alternative_facility
        self.audit(journey_id, "REFERRAL_REROUTED", alternative_facility, {"reason": reason})

    def can_close(self, journey_id: str) -> bool:
        j = self.journeys.get(journey_id)
        if not j:
            return False
        # Journey can only close if follow-up is completed and no pending external orders
        return j.state == State.FOLLOW_UP_ACTIVE and not j.pending_external

    def close(self, journey_id: str, event_id: str = "close-001") -> str:
        if not self.can_close(journey_id):
            raise ValueError("Closure gates not satisfied: Journey must be in FOLLOW_UP_ACTIVE with 0 pending external dependencies.")
        j = self.journeys[journey_id]
        j.closed_at = datetime.now(timezone.utc)
        return self.transition(journey_id, State.CLOSED, event_id, "CAREFLOW", {"closure": "validated"})


class MockIntegration:
    """Mock integration double with configurable latency, failure, and degradation modes."""

    def __init__(self):
        self.failure = "NONE"
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def call(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, payload))
        if self.failure == "TIMEOUT":
            return {"status": "PENDING", "reason": "EXTERNAL_GATEWAY_TIMEOUT", "retryable": True}
        if self.failure == "UNAVAILABLE":
            return {"status": "FAILED", "reason": "SERVICE_UNAVAILABLE", "retryable": True}
        if self.failure == "CONSENT_DENIED":
            return {"status": "CONSENT_BLOCKED", "reason": "PATIENT_DENIED_CONSENT", "retryable": False}
        return {
            "status": "SUCCESS",
            "reference": f"MOCK-{len(self.calls):04d}",
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "confidence": 1.0
        }
