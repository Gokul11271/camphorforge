# CareFlow Disaster Recovery & Business Continuity Runbook

---

## 1. Objectives & Metrics
- **Recovery Point Objective (RPO)**: $< 5\text{ minutes}$ (Transactional Outbox and WAL replication).
- **Recovery Time Objective (RTO)**: $< 15\text{ minutes}$ (Automated container failover & multi-zone DB switchover).

---

## 2. Backup Strategy
1. **PostgreSQL Database**:
   - Continuous WAL archiving to secure S3/Blob storage with KMS encryption.
   - Daily automated logical snapshot with SHA-256 integrity verification.
2. **Audit & Event Ledger**:
   - Write-once-read-many (WORM) append-only storage for immutable audit trails.
3. **Configuration & Secrets**:
   - Infrastructure-as-code versioned in Git; secrets stored in Vault with automated rotation.

---

## 3. Disaster Failover Procedure
```
PRIMARY OUTAGE DETECTED
           │
           ▼
[Step 1] Health check alert fires (3 consecutive failures over 60s)
           │
           ▼
[Step 2] Promote Hot Standby Database in Secondary Region
           │
           ▼
[Step 3] Update DNS / API Gateway routing to Secondary Cluster
           │
           ▼
[Step 4] Replay Outbox Events from last verified checkpoint
           │
           ▼
[Step 5] Verify ABDM Gateway webhook connectivity & token renewal
           │
           ▼
SYSTEM RESTORED (Estimated Total Time: 8.5 minutes)
```

---

## 4. Message Replay & Data Reconciliation
In case of message queue degradation:
1. Identify quarantined events in `quarantine_ledger`.
2. Execute idempotency-safe replay command:
   ```bash
   python scripts/replay_quarantine.py --since="2026-09-15T09:00:00Z"
   ```
3. Verified idempotency keys ensure zero duplicate clinical actions or double bookings.
