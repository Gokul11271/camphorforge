"""
National Health Programme Connectors
Integrates NP-NCD, RCH/ANMOL, U-WIN, and Nikshay into CareFlow orchestration while preserving programme ownership.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from freshness import FreshnessClass, FreshnessMetadata


class NpNcdConnector:
    """National Programme for Prevention & Control of Non-Communicable Diseases (NP-NCD)."""

    def get_patient_ncd_profile(self, ncd_id: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "programme": "NP-NCD",
            "ncd_id": ncd_id,
            "cbac_score": 6,  # High risk (>4)
            "conditions": ["HYPERTENSION_STAGE_2", "DIABETES_SUSPECTED"],
            "last_screening_date": (now - timedelta(days=14)).strftime("%Y-%m-%d"),
            "target_facility": "PHC_Kariamangalam",
            "freshness": FreshnessMetadata.create(
                source_system="NP_NCD_PORTAL",
                source_record_id=ncd_id,
                data_type="ncd_profile",
                freshness_class=FreshnessClass.CLASS_C_PERIODIC_BATCH,
                observed_at=now - timedelta(days=14)
            )
        }


class RchAnmolConnector:
    """Reproductive and Child Health (RCH) / ANMOL Programme."""

    def get_anc_profile(self, rch_id: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "programme": "RCH_ANMOL",
            "rch_id": rch_id,
            "gravida": 2,
            "parity": 1,
            "gestational_age_weeks": 28,
            "high_risk_pregnancy": True,
            "hrp_reasons": ["SEVERE_ANEMIA", "GESTATIONAL_HYPERTENSION"],
            "edd": (now + timedelta(days=84)).strftime("%Y-%m-%d"),
            "freshness": FreshnessMetadata.create(
                source_system="RCH_ANMOL_PORTAL",
                source_record_id=rch_id,
                data_type="maternal_health",
                freshness_class=FreshnessClass.CLASS_C_PERIODIC_BATCH,
                observed_at=now - timedelta(days=3)
            )
        }


class UWinConnector:
    """Universal Immunization Programme (U-WIN)."""

    def get_immunization_due(self, beneficiary_id: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "programme": "U-WIN",
            "beneficiary_id": beneficiary_id,
            "child_age_months": 9,
            "due_vaccines": ["MR_DOSE_1", "JE_DOSE_1", "VITAMIN_A_DOSE_1"],
            "session_site": "Anganwadi_Centre_04_Pennagaram",
            "next_session_date": (now + timedelta(days=5)).strftime("%Y-%m-%d"),
            "freshness": FreshnessMetadata.create(
                source_system="U_WIN_PORTAL",
                source_record_id=beneficiary_id,
                data_type="immunization_record",
                freshness_class=FreshnessClass.CLASS_C_PERIODIC_BATCH,
                observed_at=now - timedelta(days=1)
            )
        }


class NikshayConnector:
    """National Tuberculosis Elimination Programme (Nikshay)."""

    def get_tb_treatment_card(self, nikshay_id: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        return {
            "programme": "NIKSHAY",
            "nikshay_id": nikshay_id,
            "tb_type": "PULMONARY_MICROBIOLOGICALLY_CONFIRMED",
            "regimen": "FDC_4_DRUG",
            "phase": "CONTINUATION_PHASE",
            "adherence_percentage": 92.5,
            "cbnaat_result": "MTB_DETECTED_RIF_SENSITIVE",
            "dbt_nikshay_poshan_status": "CREDITED",
            "freshness": FreshnessMetadata.create(
                source_system="NIKSHAY_NTEP_GATEWAY",
                source_record_id=nikshay_id,
                data_type="tb_treatment_card",
                freshness_class=FreshnessClass.CLASS_B_NEAR_REAL_TIME,
                observed_at=now - timedelta(hours=6)
            )
        }
