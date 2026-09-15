"""
CareFlow AI Decision Support & Capability-Aware Matching Engine
Implements explainable clinical decision support, freshness-weighted facility ranking,
referral drop-off prediction, and strict clinical safety guardrails.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from freshness import FreshnessClass, FreshnessMetadata, VerificationStatus


@dataclass
class FacilityCandidate:
    facility_id: str
    facility_name: str
    facility_type: str  # DH, SDH, CHC, PHC, MC
    district: str
    distance_km: float
    specialties_available: set[str]
    diagnostics_available: set[str]
    bed_occupancy_percent: float
    active_appointment_slots: int
    scheme_empanelment: set[str]  # CMCHIS, MJPJAY, PM_JAY
    transport_corridor_feasible: bool
    freshness: FreshnessMetadata


@dataclass
class FacilityRecommendation:
    rank: int
    facility_id: str
    facility_name: str
    overall_score: float  # 0.0 to 100.0
    is_safe_candidate: bool
    confirmation_required: bool
    rejection_reasons: list[str]
    explainable_reasons: list[str]
    freshness_badge: dict[str, Any]
    confidence_score: float


class DecisionEngine:
    """Explainable AI Decision Support Engine with Freshness Penalties and Safety Guardrails."""

    def rank_facilities(
        self,
        required_specialty: str,
        required_diagnostics: list[str],
        patient_distance_baseline_km: float,
        patient_schemes: list[str],
        candidates: list[FacilityCandidate]
    ) -> list[FacilityRecommendation]:
        """Ranks regional receiving facilities using multi-criteria suitability with freshness penalties."""
        recommendations: list[FacilityRecommendation] = []

        for candidate in candidates:
            rejection_reasons = []
            explainable_reasons = []

            # 1. Hard Safety Constraints
            if required_specialty not in candidate.specialties_available:
                rejection_reasons.append(f"Missing required specialty: {required_specialty}")

            for diag in required_diagnostics:
                if diag not in candidate.diagnostics_available:
                    rejection_reasons.append(f"Missing diagnostic capability: {diag}")

            if rejection_reasons:
                recommendations.append(FacilityRecommendation(
                    rank=999,
                    facility_id=candidate.facility_id,
                    facility_name=candidate.facility_name,
                    overall_score=0.0,
                    is_safe_candidate=False,
                    confirmation_required=False,
                    rejection_reasons=rejection_reasons,
                    explainable_reasons=[],
                    freshness_badge=candidate.freshness.get_ui_badge(),
                    confidence_score=0.0
                ))
                continue

            # 2. Multi-Criteria Scoring (Max 100)
            score = 0.0

            # Clinical Fit (30 pts)
            score += 30.0
            explainable_reasons.append(f"Verified {required_specialty} department and {', '.join(required_diagnostics)} available")

            # Geographic Distance Fit (25 pts)
            dist = candidate.distance_km
            if dist <= 15:
                score += 25.0
                explainable_reasons.append(f"Close proximity ({dist:.1f} km)")
            elif dist <= 35:
                score += 18.0
                explainable_reasons.append(f"Moderate distance ({dist:.1f} km)")
            else:
                score += 10.0
                explainable_reasons.append(f"Higher travel distance ({dist:.1f} km)")

            # Appointment & Capacity Fit (15 pts)
            if candidate.active_appointment_slots > 0 and candidate.bed_occupancy_percent < 85:
                score += 15.0
                explainable_reasons.append(f"Immediate OPD slot available (bed occupancy {candidate.bed_occupancy_percent:.0f}%)")
            elif candidate.bed_occupancy_percent >= 90:
                score += 5.0
                explainable_reasons.append(f"High bed occupancy ({candidate.bed_occupancy_percent:.0f}%)")
            else:
                score += 10.0

            # Scheme Empanelment (10 pts)
            matched_schemes = set(patient_schemes).intersection(candidate.scheme_empanelment)
            if matched_schemes:
                score += 10.0
                explainable_reasons.append(f"Cashless treatment eligible under {', '.join(matched_schemes)}")

            # Transport Feasibility (10 pts)
            if candidate.transport_corridor_feasible:
                score += 10.0
                explainable_reasons.append("108 / 102 transport corridor active")

            # Data Freshness & Confidence (10 pts)
            is_fresh = candidate.freshness.is_fresh()
            confirmation_req = not is_fresh
            if is_fresh:
                score += round(10.0 * candidate.freshness.confidence, 1)
                explainable_reasons.append(f"Operational status verified {candidate.freshness.get_ui_badge()['badge_text']}")
            else:
                score += 2.0  # Heavy penalty for stale telemetry
                explainable_reasons.append("Telemetry stale (>30m) — Frontline telephone confirmation required")

            recommendations.append(FacilityRecommendation(
                rank=1,
                facility_id=candidate.facility_id,
                facility_name=candidate.facility_name,
                overall_score=round(score, 1),
                is_safe_candidate=True,
                confirmation_required=confirmation_req,
                rejection_reasons=[],
                explainable_reasons=explainable_reasons,
                freshness_badge=candidate.freshness.get_ui_badge(),
                confidence_score=candidate.freshness.confidence
            ))

        # Sort valid candidates by score descending
        valid = [r for r in recommendations if r.is_safe_candidate]
        invalid = [r for r in recommendations if not r.is_safe_candidate]
        valid.sort(key=lambda x: x.overall_score, reverse=True)

        for i, rec in enumerate(valid, 1):
            rec.rank = i

        return valid + invalid

    def predict_referral_drop_off_risk(
        self,
        travel_distance_km: float,
        has_transport_booked: bool,
        has_escort: bool,
        urgency: str
    ) -> dict[str, Any]:
        """Calculates referral drop-off risk to prioritize ASHA assisted accompaniment."""
        risk_score = 0.15  # Baseline
        contributing_factors = []

        if travel_distance_km > 30:
            risk_score += 0.35
            contributing_factors.append(f"Long travel distance ({travel_distance_km:.1f} km)")
        elif travel_distance_km > 15:
            risk_score += 0.15

        if not has_transport_booked:
            risk_score += 0.25
            contributing_factors.append("No confirmed transport / public transit dependency")

        if not has_escort:
            risk_score += 0.15
            contributing_factors.append("Unaccompanied patient / requires ASHA escort")

        if urgency == "EMERGENCY":
            risk_score += 0.10
            contributing_factors.append("High urgency clinical condition")

        risk_score = min(0.95, round(risk_score, 2))
        risk_category = "HIGH" if risk_score >= 0.60 else ("MODERATE" if risk_score >= 0.35 else "LOW")

        return {
            "drop_off_risk_score": risk_score,
            "risk_category": risk_category,
            "requires_asha_escort": risk_score >= 0.60,
            "contributing_factors": contributing_factors,
            "recommended_action": "Assign ASHA worker for accompanied referral transit" if risk_score >= 0.60 else "Routine SMS reminder"
        }
