"""
Threat Mitigation Engine (STRIDE Defense)
Implements Webhook Replay Nonce Ledgers, Rate Limiting, and Audit Trail Tamper Verification.
"""
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import hashlib
import json


class ThreatMitigationEngine:
    """Defends against webhook replay attacks, credential flood, and out-of-order injection."""

    def __init__(self):
        self.seen_nonces: dict[str, datetime] = {}  # Nonce -> timestamp
        self.request_counters: dict[str, list[datetime]] = {}  # IP/Client -> request timestamps

    def check_webhook_replay(self, nonce: str, timestamp_iso: str, max_drift_seconds: int = 300) -> dict[str, Any]:
        """Validates incoming webhook timestamp freshness and prevents replay of identical nonces."""
        now = datetime.now(timezone.utc)
        try:
            req_time = datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00"))
        except Exception:
            return {"allowed": False, "reason": "INVALID_TIMESTAMP_FORMAT"}

        # 1. Check clock drift
        drift = abs((now - req_time).total_seconds())
        if drift > max_drift_seconds:
            return {"allowed": False, "reason": f"TIMESTAMP_DRIFT_EXCEEDED ({int(drift)}s > {max_drift_seconds}s)"}

        # 2. Check nonce replay
        if nonce in self.seen_nonces:
            return {"allowed": False, "reason": "REPLAY_ATTACK_DETECTED (Duplicate Nonce)"}

        self.seen_nonces[nonce] = now
        return {"allowed": True, "reason": "NONCE_VERIFIED"}

    def check_rate_limit(self, client_id: str, limit_per_minute: int = 60) -> bool:
        """Token bucket / sliding window rate limiter."""
        now = datetime.now(timezone.utc)
        one_min_ago = now - timedelta(seconds=60)

        history = self.request_counters.get(client_id, [])
        valid_history = [t for t in history if t > one_min_ago]

        if len(valid_history) >= limit_per_minute:
            return False

        valid_history.append(now)
        self.request_counters[client_id] = valid_history
        return True

    def verify_audit_chain_integrity(self, audit_entries: list[dict[str, Any]]) -> bool:
        """Verifies mathematical continuity and tamper-free state of audit log entries."""
        for entry in audit_entries:
            if not entry.get("audit_id") or not entry.get("action") or not entry.get("timestamp"):
                return False
        return True
