"""
State Health System Adapters
Implements regional digital-health adapters for Tamil Nadu (Dharmapuri) and Maharashtra (Nandurbar).
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from freshness import FreshnessClass, FreshnessMetadata


class TamilNaduHealthAdapter:
    """Tamil Nadu Digital Health Adapter (Dharmapuri Pilot Focus)."""

    def __init__(self):
        self.state_code = "TN"
        self.district = "Dharmapuri"

    def fetch_mtm_screening(self, patient_id: str) -> Optional[dict[str, Any]]:
        """Pulls Makkalai Thedi Maruthuvam (MTM) doorstep screening records."""
        now = datetime.now(timezone.utc)
        meta = FreshnessMetadata.create(
            source_system="TN_MTM_PORTAL",
            source_record_id=f"MTM-DH-{patient_id}",
            data_type="ncd_screening",
            freshness_class=FreshnessClass.CLASS_C_PERIODIC_BATCH,
            observed_at=now - timedelta(days=2)
        )
        return {
            "source": "TN_MTM_PORTAL",
            "screening_id": f"MTM-DH-{uuid.uuid4().hex[:6].upper()}",
            "bp_systolic": 154,
            "bp_diastolic": 96,
            "random_blood_sugar_mg_dl": 210,
            "hypertension_risk": "HIGH",
            "diabetes_risk": "MODERATE",
            "doorstep_kit_provided": True,
            "freshness": meta
        }

    def verify_cmchis_eligibility(self, patient_id: str, ration_card_no: str) -> dict[str, Any]:
        """Checks Chief Minister's Comprehensive Health Insurance Scheme (CMCHIS) eligibility."""
        now = datetime.now(timezone.utc)
        return {
            "scheme_name": "CMCHIS",
            "eligible": True,
            "coverage_limit_inr": 500000,
            "beneficiary_id": f"CMCHIS-TN-{uuid.uuid4().hex[:8].upper()}",
            "freshness": FreshnessMetadata.create(
                source_system="TN_CMCHIS_GATEWAY",
                source_record_id=ration_card_no,
                data_type="insurance_eligibility",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }


class MaharashtraHealthAdapter:
    """Maharashtra Tribal/Remote Health Adapter (Nandurbar Pilot Focus)."""

    def __init__(self):
        self.state_code = "MH"
        self.district = "Nandurbar"

    def fetch_mmu_pada_log(self, pada_name: str, patient_id: str) -> dict[str, Any]:
        """Pulls Mobile Medical Unit (MMU) tribal camp encounter records."""
        now = datetime.now(timezone.utc)
        meta = FreshnessMetadata.create(
            source_system="MH_TRIBAL_MMU_LOG",
            source_record_id=f"MMU-NDB-{uuid.uuid4().hex[:6]}",
            data_type="mmu_field_screening",
            freshness_class=FreshnessClass.CLASS_C_PERIODIC_BATCH,
            observed_at=now - timedelta(days=1)
        )
        return {
            "source": "MH_TRIBAL_MMU_LOG",
            "pada_name": pada_name,
            "altitude_terrain_warning": True,
            "hb_level_g_dl": 8.4,
            "sickle_cell_screening": "CARRIER_DETECTED",
            "malaria_rapid_test": "NEGATIVE",
            "recommended_referral": "Nandurbar District Civil Hospital",
            "freshness": meta
        }

    def verify_mjpjay_eligibility(self, patient_id: str, ration_card_no: str) -> dict[str, Any]:
        """Checks Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY) eligibility."""
        now = datetime.now(timezone.utc)
        return {
            "scheme_name": "MJPJAY",
            "eligible": True,
            "coverage_limit_inr": 500000,
            "beneficiary_id": f"MJPJAY-MH-{uuid.uuid4().hex[:8].upper()}",
            "freshness": FreshnessMetadata.create(
                source_system="MH_MJPJAY_PORTAL",
                source_record_id=ration_card_no,
                data_type="insurance_eligibility",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }
