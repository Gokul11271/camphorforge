# CareFlow: Rural Care Access & Continuity Orchestration Platform
*(Care Orchestration Platform)*

> **"Existing systems provide domain services and records; our platform coordinates the complete, closed-loop care journey."**

---

## 1. Project Overview & Architectural Thesis
**CareFlow** is an enterprise-grade, **source-aware, event-driven care orchestration and interoperability platform** built to eliminate rural healthcare fragmentation across India. It connects existing public and private digital-health systems—including **ABDM (Ayushman Bharat Digital Mission)**, **UHI (Unified Health Interface)**, **eSanjeevani**, **NP-NCD**, **RCH / ANMOL**, **U-WIN**, **Nikshay**, **DVDMS / e-Aushadhi**, **108 / 102 EMS**, and **State HMIS/LIS**—into a single continuous patient care journey.

> **Engineering Reality Notice**: The core platform, interoperability boundaries, source-aware orchestration logic, security controls, and failure-handling workflows have been implemented and verified against automated synthetic/mock integration testbeds. External production interoperability remains environment- and authorization-dependent.

---

## 2. Key Architectural Invariants

1. **Federated Interoperability vs. Centralized Database**: ABDM is treated according to its federated design (identity, registries, consent, and consented health record exchange), rather than an assumed central real-time database.
2. **Five-Tier Data Freshness Engine**: Every piece of external operational data is classified into:
   - **Class A (Transaction-Real-Time)**: Transaction-generated events (Referral accept, booking, consent callback, 108 dispatch).
   - **Class B (Near-Real-Time)**: Frequent polling/webhook telemetry (Bed occupancy, lab queue, medicine stock).
   - **Class C (Periodic / Batch)**: Scheduled batch syncs (MTM screening records, HMIS reports).
   - **Class D (Static Reference)**: Master registries (HFR facility registry, HPR doctor registry).
   - **Class U (Unknown / Unverified)**: Source capability or operational status cannot be determined.
3. **Three Data Reality Tiers**:
   - `REAL_EXTERNAL`: Authorized live external system.
   - `SANDBOX_EXTERNAL`: Official government sandbox testbed (`dev.abdm.gov.in`).
   - `SIMULATED`: Local contract mock / synthetic double.
4. **Data Provenance & UI Transparency**: Explicit timestamps and confidence scores accompany all recommendations (e.g., *"Cardiology available — verified 2m ago"* vs *"Availability cannot be confirmed (Last verified 42m ago) — Action: Call facility"*).
5. **Clinical Safety & Non-Autonomous AI**: AI provides explainable decision support (referral drop-off prediction, freshness-weighted facility ranking, diagnostic SLA breach detection) with mandatory clinician supervision.

---

## 3. Integration Reality & Maturity Ledger

For full details, see the [Integration Reality Matrix](file:///d:/camphorforge/docs/INTEGRATION_REALITY_MATRIX.md).

| Subsystem | Maturity Level | Status | Data Freshness | Next Verification Step |
|---|---|---|---|---|
| **ABDM Gateway** | Level 3 | Automated Double Verified | Class A (Transaction) | Run live session & consent on `dev.abdm.gov.in` |
| **ABDM FHIR IG 6.5.0** | Level 3 | Schema Aligned | Class A (On Exchange) | Full validation with `ndhm.in#6.5.0` package |
| **UHI Open Protocol** | Level 2 | Protocol Double (v0.0.1) | Class B (Provider Dep.) | Await NHA UHI network registry |
| **eSanjeevani Hub** | Level 2 | Interface Double | Class A (Workflow Dep.) | Apply for state API gateway onboarding |
| **NP-NCD & RCH/ANMOL** | Level 2 | Synthetic Reference | Class C (Batch) | State-level batch sync agreement |
| **Hospital LIS & Pharmacy** | Level 3 | Local Double Verified | Class B (Near-Real-Time) | Facility HL7/FHIR deployment |
| **108 / 102 EMS Transport** | Level 3 | Local Double (Live GPS Mode) | Class A (Mode Dep.) | State 108 CAD API handshake |

---

## 4. Canonical 14-Stage Patient Journey

```
NEW ──► TRIAGED ──► CONSULTATION_REQUIRED ──► CONSULTED ──► DIAGNOSTIC_REQUIRED
                                                                 │
                                                                 ▼
REFERRAL_REQUIRED ◄── DIAGNOSTIC_COMPLETED ◄── DIAGNOSTIC_IN_PROGRESS
       │
       ▼
REFERRAL_ACCEPTED ──► APPOINTMENT_CONFIRMED ──► TRANSPORT_CONFIRMED ──► PATIENT_ARRIVED
                                                                             │
                                                                             ▼
CLOSED ◄── FOLLOW_UP_ACTIVE ◄── MEDICINE_FULFILLED ◄── TREATMENT_COMPLETED
```

---

## 5. Master Automated Validation Suite Execution

To execute the 5-bucket reality-aware validation suite:

```bash
python tests/run_tests.py
```

### Execution Summary:
```text
================================================================================
                       TEST EXECUTION BUCKET SUMMARY
================================================================================
Bucket 1: Core Workflow & State Machine             : 4/4 PASS
Bucket 2: Freshness, Provenance & Reality Engine    : 3/3 PASS
Bucket 3: ABDM FHIR Profile Alignment               : 5/5 PASS
Bucket 4: Adapter Logic & Chaos Scenarios           : 17/17 PASS
Bucket 5: Security, RBAC & DPDP Controls            : 5/5 PASS
--------------------------------------------------------------------------------
INTERNAL TESTBED SUITE TOTAL: 34/34 PASSED (100% Pass Rate)
================================================================================
```

---

## 6. Accessing the Interactive Web Application
Open `frontend/index.html` in any web browser to explore:
- Multi-role switching (**Frontline CHO/ASHA**, **Doctor**, **Referral Coordinator**, **Patient**, **District Command Centre**).
- Dedicated **Integration Reality Matrix** tab.
- Native localization in **English**, **Tamil (தமிழ்)**, **Hindi (हिंदी)**, and **Marathi (मराठी)**.
- Interactive **Simulation Console** for real-time journey stepping, offline sync replay, and referral rerouting.
