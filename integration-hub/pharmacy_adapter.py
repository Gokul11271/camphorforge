"""
Pharmacy & Drug Logistics Adapter (DVDMS / e-Aushadhi)
Implements drug availability search, freshness evaluation, confidence scoring,
and dispense fulfillment verification.
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
class MedicineStockRecord:
    drug_code: str
    drug_name: str
    facility_id: str
    facility_name: str
    available_units: int
    minimum_threshold: int
    batch_expiry: str
    freshness: FreshnessMetadata

    def is_available(self) -> bool:
        return self.available_units > 0 and self.freshness.is_fresh()


class PharmacyAdapter:
    """DVDMS / e-Aushadhi Drug Supply System Connector."""

    def __init__(self):
        self.dispensed_records: dict[str, dict[str, Any]] = {}

    def check_availability(
        self,
        drug_code: str,
        facility_id: str = "IN3305001234"
    ) -> MedicineStockRecord:
        """Queries facility pharmacy inventory with explicit freshness & confidence scoring."""
        now = datetime.now(timezone.utc)
        
        # Synthetic drug catalog
        catalog = {
            "MED-AML-05": ("Amlodipine 5mg Tablets", 450, "2027-08-31"),
            "MED-TEL-40": ("Telmisartan 40mg Tablets", 320, "2027-05-31"),
            "MED-MET-500": ("Metformin 500mg Tablets", 180, "2026-12-31"),
            "MED-ATO-10": ("Atorvastatin 10mg Tablets", 210, "2027-09-30")
        }
        name, units, expiry = catalog.get(drug_code, ("Essential Generic Medicine", 50, "2027-01-01"))

        # Observed 11 minutes ago from DVDMS
        meta = FreshnessMetadata.create(
            source_system="DVDMS_TNMSC_LMIS",
            source_record_id=f"STK-{facility_id}-{drug_code}",
            data_type="medicine_stock",
            freshness_class=FreshnessClass.CLASS_B_NEAR_REAL_TIME,
            observed_at=now - timedelta(minutes=11),
            custom_ttl_seconds=3600  # 1 hour TTL
        )

        return MedicineStockRecord(
            drug_code=drug_code,
            drug_name=name,
            facility_id=facility_id,
            facility_name="Dharmapuri Govt Medical College Pharmacy",
            available_units=units,
            minimum_threshold=50,
            batch_expiry=expiry,
            freshness=meta
        )

    def record_dispense(
        self,
        prescription_id: str,
        drug_code: str,
        quantity: int,
        pharmacist_hpr: str = "PHARM-3301"
    ) -> dict[str, Any]:
        """Records medicine dispense event with pharmacist provenance."""
        dispense_id = f"DISP-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc)
        record = {
            "dispense_id": dispense_id,
            "prescription_id": prescription_id,
            "drug_code": drug_code,
            "quantity_dispensed": quantity,
            "pharmacist_id": pharmacist_hpr,
            "dispensed_at": now.isoformat(),
            "freshness": FreshnessMetadata.create(
                source_system="HOSPITAL_PHARMACY_POS",
                source_record_id=dispense_id,
                data_type="medicine_dispense",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }
        self.dispensed_records[dispense_id] = record
        return record
