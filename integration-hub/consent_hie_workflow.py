"""
Consented Health Information Exchange (HIE-CM) Workflow Orchestrator
Enforces DPDP compliance, patient consent verification, FHIR conformance gates,
and immutable data provenance logging.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from careflow_fhir.conformance import validate_bundle, validate_resource
from src.freshness import FreshnessClass, FreshnessMetadata


class ConsentStatus:
    REQUESTED = "REQUESTED"
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


@dataclass
class ConsentRecord:
    consent_id: str
    patient_id: str
    purpose: str
    hi_types: list[str]
    status: str
    granted_at: Optional[datetime]
    expires_at: Optional[datetime]
    revoked_at: Optional[datetime] = None


class ConsentHieOrchestrator:
    """Consented Health Information Exchange Orchestrator."""

    def __init__(self):
        self.consents: dict[str, ConsentRecord] = {}
        self.imported_records: list[dict[str, Any]] = []
        self.quarantine_ledger: list[dict[str, Any]] = []

    def create_consent_request(
        self,
        patient_id: str,
        purpose: str = "CAREMGT",
        hi_types: Optional[list[str]] = None,
        validity_days: int = 30
    ) -> ConsentRecord:
        consent_id = f"CR-{uuid.uuid4().hex[:8].upper()}"
        rec = ConsentRecord(
            consent_id=consent_id,
            patient_id=patient_id,
            purpose=purpose,
            hi_types=hi_types or ["DiagnosticReport", "OPConsultation", "Prescription"],
            status=ConsentStatus.REQUESTED,
            granted_at=None,
            expires_at=None
        )
        self.consents[consent_id] = rec
        return rec

    def grant_consent(self, consent_id: str, validity_days: int = 30) -> ConsentRecord:
        rec = self.consents.get(consent_id)
        if not rec:
            raise KeyError(f"Consent {consent_id} not found")
        now = datetime.now(timezone.utc)
        rec.status = ConsentStatus.GRANTED
        rec.granted_at = now
        rec.expires_at = now + timedelta(days=validity_days)
        return rec

    def deny_consent(self, consent_id: str, reason: str = "PATIENT_REFUSED") -> ConsentRecord:
        rec = self.consents.get(consent_id)
        if not rec:
            raise KeyError(f"Consent {consent_id} not found")
        rec.status = ConsentStatus.DENIED
        return rec

    def revoke_consent(self, consent_id: str) -> ConsentRecord:
        rec = self.consents.get(consent_id)
        if not rec:
            raise KeyError(f"Consent {consent_id} not found")
        rec.status = ConsentStatus.REVOKED
        rec.revoked_at = datetime.now(timezone.utc)
        return rec

    def execute_hie_transfer(
        self,
        consent_id: str,
        fhir_bundle: dict[str, Any]
    ) -> dict[str, Any]:
        """Validates consent and ingests FHIR bundle with strict conformance gate."""
        rec = self.consents.get(consent_id)
        now = datetime.now(timezone.utc)

        # 1. Check consent validity
        if not rec:
            return {"status": "BLOCKED", "reason": "CONSENT_NOT_FOUND"}
        if rec.status != ConsentStatus.GRANTED:
            return {"status": "BLOCKED", "reason": f"CONSENT_{rec.status}"}
        if rec.expires_at and now > rec.expires_at:
            rec.status = ConsentStatus.EXPIRED
            return {"status": "BLOCKED", "reason": "CONSENT_EXPIRED"}

        # 2. Run ABDM FHIR Conformance Validator
        validation_result = validate_bundle(fhir_bundle)

        # 3. Quarantine if invalid
        if not validation_result["valid"]:
            quarantine_entry = {
                "quarantine_id": str(uuid.uuid4()),
                "consent_id": consent_id,
                "bundle_id": fhir_bundle.get("id"),
                "reason": "FHIR_CONFORMANCE_FAILURE",
                "validation_errors": validation_result["entry_reports"],
                "timestamp": now.isoformat()
            }
            self.quarantine_ledger.append(quarantine_entry)
            return {
                "status": "DATA_QUARANTINED",
                "reason": "FHIR_CONFORMANCE_FAILURE",
                "quarantine_id": quarantine_entry["quarantine_id"],
                "action": "Record excluded from clinical view until corrected"
            }

        # 4. Successful Ingestion with Provenance
        import_record = {
            "exchange_id": str(uuid.uuid4()),
            "consent_id": consent_id,
            "patient_id": rec.patient_id,
            "bundle_id": fhir_bundle.get("id"),
            "entries_count": len(fhir_bundle.get("entry", [])),
            "ingested_at": now.isoformat(),
            "status": "ACTIVE_CLINICAL_EVIDENCE",
            "freshness": FreshnessMetadata.create(
                source_system="ABDM_HIE_CM_FEDERATED_GW",
                source_record_id=consent_id,
                data_type="clinical_history_bundle",
                freshness_class=FreshnessClass.CLASS_A_TRANSACTION_REAL_TIME
            )
        }
        self.imported_records.append(import_record)
        return {"status": "SUCCESS", "exchange_id": import_record["exchange_id"], "record": import_record}
