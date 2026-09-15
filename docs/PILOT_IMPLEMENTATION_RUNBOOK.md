# CareFlow Pilot Implementation Runbook
## Deployments: Tamil Nadu (Dharmapuri) & Maharashtra (Nandurbar)

---

## 1. Pilot Track 1: Tamil Nadu (Dharmapuri District)
*Stress Condition: Continuity across a mature public health digital ecosystem*

### Facility Hierarchy
1. **Sub-Centre / AAM**: Karimangalam AAM, Pennagaram Rural SC.
2. **Primary Health Centre (PHC)**: Karimangalam PHC, Indur PHC.
3. **Taluk / Sub-District Hospital (SDH)**: Pennagaram Taluk Hospital, Harur SDH.
4. **District Hospital / Medical College**: Dharmapuri Government Medical College Hospital (HFR: `IN3305001234`).

### Integrated Digital Platforms
- **MTM (Makkalai Thedi Maruthuvam)**: Ingests doorstep screening for hypertension & diabetes.
- **TNPHC / UHS**: Regional facility and practitioner master registries.
- **DVDMS (TNMSC)**: District drug warehouse and hospital pharmacy inventory feeds.
- **CMCHIS**: Chief Minister's Comprehensive Health Insurance Scheme eligibility checks.
- **108 EMS**: Emergency transport corridor dispatch and GPS updates.

---

## 2. Pilot Track 2: Maharashtra (Nandurbar District)
*Stress Condition: Remote tribal terrain, intermittent connectivity, long travel distances*

### Facility Hierarchy
1. **Remote Pada / MMU Camp**: Dhadgaon Pada 4, Akrani Tribal Hamlet.
2. **Ayushman Arogya Mandir (AAM)**: Molgi AAM, Bilgaon AAM.
3. **Rural Hospital (RH)**: Dhadgaon Rural Hospital, Akkalkuwa RH.
4. **District Civil Hospital**: Nandurbar District Civil Hospital (HFR: `IN2705009876`).

### Operational Workflows
- **Offline Field Sync**: Frontline workers capture vitals and referral requests offline; sync via vector-clock ledger upon reaching network coverage at RH.
- **102 Janani Shishu Express & 108 EMS**: Transport coordination linked directly to high-risk maternal (RCH) and sickle-cell referrals.
- **MJPJAY**: Mahatma Jyotirao Phule Jan Arogya Yojana coverage verification.
