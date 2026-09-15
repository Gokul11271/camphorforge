"""
eSanjeevani Teleconsultation Adapter
Implements assisted telemedicine referral, virtual consultation room linkage,
status tracking, prescription extraction, and encounter closure.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from freshness import FreshnessClass, FreshnessMetadata


@dataclass
class TeleconsultationSession:
    session_id: str
    referral_id: str
    patient_id: str
    doctor_hpr_id: str
    facility_hfr_id: str
    specialty: str
    room_url: str
    access_token: str
    status: str  # SCHEDULED, IN_PROGRESS, COMPLETED, NO_SHOW, CANCELLED
    scheduled_start: datetime
    freshness: FreshnessMetadata


class EsanjeevaniAdapter:
    """eSanjeevani Government Teleconsultation Platform Connector."""

    def __init__(self):
        self.sessions: dict[str, TeleconsultationSession] = {}

    def schedule_consultation(
        self,
        referral_id: str,
        patient_id: str,
        patient_name: str,
        specialty: str = "General Medicine",
        preferred_time: Optional[datetime] = None
    ) -> TeleconsultationSession:
        """Schedules an assisted teleconsultation session with a government specialist."""
        session_id = f"ESANJ-{uuid.uuid4().hex[:8].upper()}"
        start_time = preferred_time or (datetime.now(timezone.utc) + timedelta(minutes=30))
        room_token = uuid.uuid4().hex[:24]

        meta = FreshnessMetadata.create(
            source_system="eSanjeevani_National_Hub",
            source_record_id=session_id,
            data_type="teleconsultation_session",
            freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
        )

        session = TeleconsultationSession(
            session_id=session_id,
            referral_id=referral_id,
            patient_id=patient_id,
            doctor_hpr_id="HPR-DR-44021",
            facility_hfr_id="IN3305001234",
            specialty=specialty,
            room_url=f"https://esanjeevani.in/hub/room/{session_id}?token={room_token}",
            access_token=room_token,
            status="SCHEDULED",
            scheduled_start=start_time,
            freshness=meta
        )
        self.sessions[session_id] = session
        return session

    def complete_consultation(
        self,
        session_id: str,
        clinical_notes: str,
        prescribed_meds: list[str],
        recommended_tests: list[str]
    ) -> dict[str, Any]:
        """Processes doctor completion callback from eSanjeevani."""
        session = self.sessions.get(session_id)
        if not session:
            raise KeyError(f"Session {session_id} not found")

        session.status = "COMPLETED"
        now = datetime.now(timezone.utc)

        return {
            "session_id": session_id,
            "status": "COMPLETED",
            "completed_at": now.isoformat(),
            "clinical_notes": clinical_notes,
            "prescriptions": prescribed_meds,
            "diagnostic_orders": recommended_tests,
            "freshness": FreshnessMetadata.create(
                source_system="eSanjeevani_National_Hub",
                source_record_id=session_id,
                data_type="consultation_summary",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }
