"""
Laboratory Information System (LIS) Adapter
Implements diagnostic test ordering, specimen intake tracking, result delivery,
and critical value alert triggers.
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
class DiagnosticOrderResult:
    order_id: str
    journey_id: str
    test_code: str
    test_name: str
    facility_id: str
    status: str  # ORDERED, SPECIMEN_COLLECTED, PROCESSING, COMPLETED, DELAYED
    is_critical: bool
    result_value: Optional[str]
    reference_range: Optional[str]
    ordered_at: datetime
    completed_at: Optional[datetime]
    sla_hours: int
    freshness: FreshnessMetadata


class LisAdapter:
    """Diagnostic Laboratory Information System Connector."""

    def __init__(self):
        self.orders: dict[str, DiagnosticOrderResult] = {}

    def submit_order(
        self,
        journey_id: str,
        test_code: str,
        test_name: str,
        facility_id: str = "IN3305001234",
        sla_hours: int = 4
    ) -> DiagnosticOrderResult:
        """Submits lab order to facility LIS."""
        order_id = f"LIS-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)

        meta = FreshnessMetadata.create(
            source_system="DISTRICT_HOSPITAL_LIS",
            source_record_id=order_id,
            data_type="diagnostic_queue",
            freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
        )

        record = DiagnosticOrderResult(
            order_id=order_id,
            journey_id=journey_id,
            test_code=test_code,
            test_name=test_name,
            facility_id=facility_id,
            status="ORDERED",
            is_critical=False,
            result_value=None,
            reference_range=None,
            ordered_at=now,
            completed_at=None,
            sla_hours=sla_hours,
            freshness=meta
        )
        self.orders[order_id] = record
        return record

    def update_specimen_collected(self, order_id: str, specimen_barcode: str) -> dict[str, Any]:
        """Updates status to specimen collected."""
        rec = self.orders.get(order_id)
        if not rec:
            raise KeyError(f"Order {order_id} not found")
        rec.status = "SPECIMEN_COLLECTED"
        return {"order_id": order_id, "status": "SPECIMEN_COLLECTED", "barcode": specimen_barcode}

    def publish_result(
        self,
        order_id: str,
        result_value: str,
        reference_range: str,
        is_critical: bool = False
    ) -> DiagnosticOrderResult:
        """Publishes lab result and flags critical findings."""
        rec = self.orders.get(order_id)
        if not rec:
            raise KeyError(f"Order {order_id} not found")

        rec.status = "COMPLETED"
        rec.result_value = result_value
        rec.reference_range = reference_range
        rec.is_critical = is_critical
        rec.completed_at = datetime.now(timezone.utc)
        rec.freshness = FreshnessMetadata.create(
            source_system="DISTRICT_HOSPITAL_LIS",
            source_record_id=order_id,
            data_type="lab_result",
            freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
        )
        return rec
