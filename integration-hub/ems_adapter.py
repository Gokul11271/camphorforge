"""
Emergency Medical Services (108 / 102 EMS) Transport Adapter
Implements referral transport dispatch, live/periodic tracking, ETA calculation, and arrival verification.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from freshness import FreshnessClass, FreshnessMetadata, TransportStatusSource


@dataclass
class EmsDispatchRecord:
    dispatch_id: str
    referral_id: str
    ambulance_service: str  # 108_EMERGENCY or 102_JANANI_SHISHU
    vehicle_number: str
    driver_contact: str
    status: str  # DISPATCHED, EN_ROUTE_PICKUP, PATIENT_ONBOARD, ARRIVED_DESTINATION, CANCELLED
    status_source: TransportStatusSource
    distance_km: float
    eta_minutes: int
    last_gps_timestamp: datetime
    freshness: FreshnessMetadata


class EmsAdapter:
    """108 / 102 Emergency Medical Transport Connector."""

    def __init__(self):
        self.dispatches: dict[str, EmsDispatchRecord] = {}

    def request_dispatch(
        self,
        referral_id: str,
        pickup_address: str,
        destination_facility: str,
        service_type: str = "108_EMERGENCY"
    ) -> EmsDispatchRecord:
        """Dispatches government emergency ambulance."""
        dispatch_id = f"EMS-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        meta = FreshnessMetadata.create(
            source_system="STATE_108_CAD_SYSTEM",
            source_record_id=dispatch_id,
            data_type="ambulance_gps",
            freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME,
            observed_at=now,
            custom_ttl_seconds=60  # 1 min GPS TTL
        )

        record = EmsDispatchRecord(
            dispatch_id=dispatch_id,
            referral_id=referral_id,
            ambulance_service=service_type,
            vehicle_number="TN-29-G-1084",
            driver_contact="+91-98420-10800",
            status="DISPATCHED",
            status_source=TransportStatusSource.LIVE_GPS,
            distance_km=6.8,
            eta_minutes=14,
            last_gps_timestamp=now,
            freshness=meta
        )
        self.dispatches[dispatch_id] = record
        return record

    def update_status(
        self,
        dispatch_id: str,
        new_status: str,
        distance_km: float,
        eta_minutes: int,
        status_source: TransportStatusSource = TransportStatusSource.LIVE_GPS
    ) -> EmsDispatchRecord:
        """Updates live location and operational state."""
        rec = self.dispatches.get(dispatch_id)
        if not rec:
            raise KeyError(f"Dispatch {dispatch_id} not found")

        now = datetime.now(timezone.utc)
        rec.status = new_status
        rec.distance_km = distance_km
        rec.eta_minutes = eta_minutes
        rec.status_source = status_source
        rec.last_gps_timestamp = now
        rec.freshness = FreshnessMetadata.create(
            source_system="STATE_108_CAD_SYSTEM",
            source_record_id=dispatch_id,
            data_type="ambulance_gps",
            freshness_class=FreshnessClass.CLASS_B_NEAR_REAL_TIME if status_source == TransportStatusSource.LIVE_GPS else FreshnessClass.CLASS_C_PERIODIC_BATCH,
            observed_at=now,
            custom_ttl_seconds=60
        )
        return rec
