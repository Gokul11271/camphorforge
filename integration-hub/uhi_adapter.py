"""
Unified Health Interface (UHI) Adapter
Implements open health network service discovery, slot availability search with freshness,
booking confirmation, and cancellation.
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
class UhiSlot:
    slot_id: str
    facility_id: str
    facility_name: str
    doctor_id: str
    doctor_name: str
    specialty: str
    start_time: datetime
    end_time: datetime
    fee_inr: float
    freshness: FreshnessMetadata


class UhiAdapter:
    """UHI Open Health Service Network Adapter."""

    def __init__(self, network_id: str = "UHI_CAREFLOW_EUA_01"):
        self.network_id = network_id
        self.bookings: dict[str, dict[str, Any]] = {}

    def search_slots(
        self,
        specialty: str,
        district: str = "Dharmapuri",
        date_str: Optional[str] = None
    ) -> list[UhiSlot]:
        """Discovers available specialist appointments across participating UHI facilities."""
        now = datetime.now(timezone.utc)
        target_date = date_str or (now + timedelta(days=1)).strftime("%Y-%m-%d")

        # Synthetic slot discovery across verified regional facilities
        facilities = [
            ("IN3305001234", "Dharmapuri Govt Medical College Hospital", "DOC3301", "Dr. A. Sundaram, MD", 0.0),
            ("IN3305002456", "Pennagaram Taluk Hospital", "DOC3302", "Dr. R. Priya, DNB", 0.0),
            ("IN3305003789", "Harur Community Health Centre", "DOC3303", "Dr. K. Murugan, MBBS", 0.0)
        ]

        slots = []
        for fac_id, fac_name, doc_id, doc_name, fee in facilities:
            slot_id = f"SLOT-{uuid.uuid4().hex[:6].upper()}"
            start_t = datetime.fromisoformat(f"{target_date}T09:30:00+00:00")
            end_t = datetime.fromisoformat(f"{target_date}T10:00:00+00:00")

            meta = FreshnessMetadata.create(
                source_system="UHI_HSPA_GATEWAY",
                source_record_id=slot_id,
                data_type="teleconsultation_slot",
                freshness_class=FreshnessClass.CLASS_B_NEAR_REAL_TIME,
                observed_at=now - timedelta(minutes=4)
            )

            slots.append(UhiSlot(
                slot_id=slot_id,
                facility_id=fac_id,
                facility_name=fac_name,
                doctor_id=doc_id,
                doctor_name=doc_name,
                specialty=specialty,
                start_time=start_t,
                end_time=end_t,
                fee_inr=fee,
                freshness=meta
            ))
        return slots

    def book_appointment(
        self,
        slot_id: str,
        patient_id: str,
        patient_name: str,
        referral_id: Optional[str] = None
    ) -> dict[str, Any]:
        """Confirms appointment booking on UHI network."""
        booking_id = f"UHI-BKG-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        record = {
            "booking_id": booking_id,
            "slot_id": slot_id,
            "patient_id": patient_id,
            "patient_name": patient_name,
            "referral_id": referral_id,
            "status": "CONFIRMED",
            "booked_at": now.isoformat(),
            "freshness": FreshnessMetadata.create(
                source_system="UHI_BPP",
                source_record_id=booking_id,
                data_type="appointment_booking",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }
        self.bookings[booking_id] = record
        return record

    def cancel_appointment(self, booking_id: str, reason: str = "PATIENT_REQUEST") -> dict[str, Any]:
        if booking_id in self.bookings:
            self.bookings[booking_id]["status"] = "CANCELLED"
            self.bookings[booking_id]["cancellation_reason"] = reason
            return {"status": "SUCCESS", "booking_id": booking_id, "state": "CANCELLED"}
        return {"status": "NOT_FOUND", "booking_id": booking_id}
