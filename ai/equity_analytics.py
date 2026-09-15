"""
Rural Health Equity Analytics Engine
Measures structural healthcare access disparities across blocks, geography, transport corridors,
and specialist availability to guide operational equity interventions.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class BlockEquityMetric:
    block_name: str
    district: str
    population: int
    avg_distance_to_dh_km: float
    specialist_coverage_ratio: float  # specialists per 100k
    transport_availability_index: float  # 0.0 to 1.0
    referral_completion_rate: float     # 0.0 to 1.0
    equity_disparity_score: float       # 0.0 (High Equity) to 1.0 (Severe Inequity)
    priority_level: str                 # CRITICAL, ELEVATED, NOMINAL


class EquityAnalyticsEngine:
    """Computes operational equity indices without collecting sensitive personal demographic data."""

    def evaluate_district_equity(self, district: str = "Dharmapuri") -> dict[str, Any]:
        """Calculates block-level equity metrics for district command centres."""
        
        # Reference pilot block datasets
        if district == "Dharmapuri":
            blocks = [
                ("Pennagaram (Hilly/Forest)", 165000, 38.5, 0.4, 0.45, 0.62),
                ("Harur (Tribal Border)", 195000, 42.0, 0.6, 0.50, 0.68),
                ("Karimangalam", 145000, 18.2, 1.2, 0.85, 0.88),
                ("Dharmapuri Urban/Semi-urban", 240000, 5.0, 4.5, 0.95, 0.94),
                ("Palacode", 175000, 24.0, 1.1, 0.78, 0.82)
            ]
        else:  # Nandurbar (Maharashtra)
            blocks = [
                ("Akrani / Dhadgaon (Satpura Hills)", 185000, 68.0, 0.2, 0.30, 0.48),
                ("Akkalkuwa (Tribal/Forest)", 210000, 54.0, 0.3, 0.38, 0.55),
                ("Nawapur", 230000, 35.0, 0.9, 0.70, 0.76),
                ("Nandurbar Urban", 260000, 4.0, 3.8, 0.92, 0.91),
                ("Shahada", 290000, 28.0, 1.4, 0.80, 0.84)
            ]

        results: list[BlockEquityMetric] = []
        for name, pop, dist, spec_ratio, trans_idx, ref_rate in blocks:
            # Disparity formula: high distance + low transport + low specialist ratio + low completion
            dist_factor = min(1.0, dist / 60.0) * 0.35
            trans_factor = (1.0 - trans_idx) * 0.25
            spec_factor = max(0.0, (2.0 - spec_ratio) / 2.0) * 0.20
            completion_factor = (1.0 - ref_rate) * 0.20

            disparity_score = round(dist_factor + trans_factor + spec_factor + completion_factor, 2)
            priority = "CRITICAL" if disparity_score >= 0.60 else ("ELEVATED" if disparity_score >= 0.40 else "NOMINAL")

            results.append(BlockEquityMetric(
                block_name=name,
                district=district,
                population=pop,
                avg_distance_to_dh_km=dist,
                specialist_coverage_ratio=spec_ratio,
                transport_availability_index=trans_idx,
                referral_completion_rate=ref_rate,
                equity_disparity_score=disparity_score,
                priority_level=priority
            ))

        # Sort by disparity descending
        results.sort(key=lambda x: x.equity_disparity_score, reverse=True)

        return {
            "district": district,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "highest_inequity_block": results[0].block_name,
            "overall_district_disparity_index": round(sum(r.equity_disparity_score for r in results) / len(results), 2),
            "block_metrics": [
                {
                    "block": r.block_name,
                    "disparity_score": r.equity_disparity_score,
                    "priority": r.priority_level,
                    "distance_km": r.avg_distance_to_dh_km,
                    "referral_completion": f"{int(r.referral_completion_rate * 100)}%",
                    "transport_index": f"{int(r.transport_availability_index * 100)}%"
                }
                for r in results
            ],
            "recommended_interventions": [
                f"Deploy additional MMU / 102 transport unit to {results[0].block_name}",
                f"Schedule bi-weekly specialist teleconsultation camp in {results[1].block_name}"
            ]
        }
