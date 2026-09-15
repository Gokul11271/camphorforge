/**
 * CareFlow Production Orchestration Frontend Application (Reality-Aware Edition)
 * Multi-role UI supporting Patient, Frontline Worker (CHO/ASHA), Doctor, Referral Desk, Command Centre, and Interactive Simulator.
 * Explicitly exposes Data Reality tiers (REAL_EXTERNAL, SANDBOX_EXTERNAL, SIMULATED) and Integration Maturity states.
 */

// Multilingual Dictionary
const I18N = {
  en: {
    appTitle: "CareFlow Orchestration Platform",
    subtitle: "Source-Aware, Reality-Transparent Rural Care Orchestration Engine",
    journeyTitle: "Active Pilot Pathway: Dharmapuri NCD Care Continuity",
    patientName: "Meenakshi Ramasamy",
    patientMeta: "ABHA: 91-4458-2910-4492 • Age 48 • Karimangalam Block, Dharmapuri",
    verifiedBadge: "Verified via State HIS [SIMULATED]",
    staleBadge: "Availability cannot be confirmed (Last verified 42m ago) — Action: Call facility",
    criticalBadge: "Critical Action Required",
    tabFrontline: "Frontline CHO Desk",
    tabDoctor: "Doctor Consultation",
    tabReferral: "Referral Desk",
    tabPatient: "Patient Portal",
    tabCommand: "District Command Centre",
    tabIntegrations: "Integration Reality Matrix",
    tabSimulation: "Live Simulation Console",
    nextAction: "Next Operational Action"
  },
  ta: {
    appTitle: "கேர்ஃபுளோ மருத்துவ ஒருங்கிணைப்பு தளம்",
    subtitle: "கிராமப்புற தொடர் சிகிச்சை அணுகல் மற்றும் உண்மைநிலை ஒருங்கிணைப்பு அமைப்பு",
    journeyTitle: "செயலில் உள்ள முன்னோடி வழித்தடம்: தருமபுரி NCD தொடர் சிகிச்சை",
    patientName: "மீனாட்சி ராமசாமி",
    patientMeta: "ABHA: 91-4458-2910-4492 • வயது 48 • காரிமங்கலம் வட்டம், தருமபுரி",
    verifiedBadge: "மாநில HIS மூலம் சரிபார்க்கப்பட்டது [SIMULATED]",
    staleBadge: "கிடைக்கும் நிலையை உறுதிப்படுத்த முடியவில்லை — மருத்துவமனையை அழைக்கவும்",
    criticalBadge: "அவசர நடவடிக்கை தேவை",
    tabFrontline: "CHO களப் பணியாளர் தளம்",
    tabDoctor: "மருத்துவர் ஆலோசனை",
    tabReferral: "பரிந்துரை மேசை",
    tabPatient: "நோயாளி போர்டல்",
    tabCommand: "மாவட்ட கட்டளை மையம்",
    tabIntegrations: "இணைப்பு நிலை மேட்ரிக்ஸ்",
    tabSimulation: "நேரடி உருவகப்படுத்துதல்",
    nextAction: "அடுத்த செயல்பாட்டு நடவடிக்கை"
  },
  hi: {
    appTitle: "केयरफ्लो स्वास्थ्य समन्वय मंच",
    subtitle: "ग्रामीण देखभाल निरंतरता और वास्तविकता-पारदर्शी समन्वय इंजन",
    journeyTitle: "सक्रिय पायलट मार्ग: धर्मपुरी गैर-संचारी रोग निरंतरता",
    patientName: "मीनाक्षी रामास्वामी",
    patientMeta: "ABHA: 91-4458-2910-4492 • आयु 48 • करीमंगलम ब्लॉक, धर्मपुरी",
    verifiedBadge: "राज्य प्रणाली द्वारा सत्यापित [SIMULATED]",
    staleBadge: "उपलब्धता की पुष्टि नहीं की जा सकी — अस्पताल से संपर्क करें",
    criticalBadge: "महत्वपूर्ण कार्रवाई आवश्यक",
    tabFrontline: "सीएचओ कार्यक्षेत्र",
    tabDoctor: "डॉक्टर परामर्श",
    tabReferral: "रेफरल डेस्क",
    tabPatient: "रोगी पोर्टल",
    tabCommand: "जिला कमान केंद्र",
    tabIntegrations: "एकीकरण वास्तविकता मैट्रिक्स",
    tabSimulation: "लाइव सिमुलेशन कंसोल",
    nextAction: "अगली परिचालन कार्रवाई"
  },
  mr: {
    appTitle: "केअरफ्लो आरोग्य समन्वय प्रणाली",
    subtitle: "ग्रामीण आरोग्य सेवा सातत्य व संदर्भ समन्वय प्लॅटफॉर्म",
    journeyTitle: "सक्रिय पायलट मार्ग: नंदुरबार / धर्मपुरी उपचार सातत्य",
    patientName: "मीनाक्षी रामास्वामी",
    patientMeta: "ABHA: 91-4458-2910-4492 • वय 48 • नंदुरबार / धर्मपुरी",
    verifiedBadge: "तपासलेले [SIMULATED]",
    staleBadge: "उपलब्धतेची खात्री देता येत नाही — संपर्क साधा",
    criticalBadge: "तातडीची कारवाई आवश्यक",
    tabFrontline: "सीएचओ कार्यक्षेत्र",
    tabDoctor: "डॉक्टर सल्लामसलत",
    tabReferral: "रेफरल डेस्क",
    tabPatient: "रुग्ण पोर्टल",
    tabCommand: "जिल्हा नियंत्रण केंद्र",
    tabIntegrations: "एकीकरण वास्तव मॅट्रिक्स",
    tabSimulation: "थेट सिम्युलेशन कन्सोल",
    nextAction: "पुढील कृती"
  }
};

const CARE_STEPS = [
  { id: "NEW", label: "Registered" },
  { id: "TRIAGED", label: "Triaged" },
  { id: "CONSULTED", label: "Consulted" },
  { id: "DIAGNOSTIC_REQUIRED", label: "Lab Ordered" },
  { id: "DIAGNOSTIC_COMPLETED", label: "Lab Ready" },
  { id: "REFERRAL_REQUIRED", label: "Referral Out" },
  { id: "REFERRAL_ACCEPTED", label: "Accepted" },
  { id: "APPOINTMENT_CONFIRMED", label: "Appointment" },
  { id: "TRANSPORT_CONFIRMED", label: "108 Transport" },
  { id: "PATIENT_ARRIVED", label: "Arrived at DH" },
  { id: "TREATMENT_COMPLETED", label: "Treated" },
  { id: "MEDICINE_FULFILLED", label: "Dispensed" },
  { id: "FOLLOW_UP_ACTIVE", label: "Follow-up" },
  { id: "CLOSED", label: "Closed" }
];

const INTEGRATIONS = [
  { name: "ABDM Gateway", maturity: "Level 3", status: "SIMULATED DOUBLE (Sandbox Configured)", freshness: "Class A (Transaction)" },
  { name: "ABDM FHIR IG 6.5.0", maturity: "Level 3", status: "SCHEMA ALIGNED", freshness: "Class A (On Exchange)" },
  { name: "UHI Protocol (0.0.1)", maturity: "Level 2", status: "PROTOCOL DOUBLE", freshness: "Class B (Provider Dep.)" },
  { name: "eSanjeevani Hub", maturity: "Level 2", status: "INTERFACE DOUBLE", freshness: "Class A (Workflow Dep.)" },
  { name: "NP-NCD & RCH/ANMOL", maturity: "Level 2", status: "SYNTHETIC REFERENCE", freshness: "Class C (Batch)" },
  { name: "Hospital LIS & Pharmacy", maturity: "Level 3", status: "LOCAL DOUBLE VERIFIED", freshness: "Class B (Near-Real-Time)" },
  { name: "108/102 EMS Transport", maturity: "Level 3", status: "LOCAL DOUBLE (Live GPS Mode)", freshness: "Class A (Mode Dep.)" }
];

class CareFlowApp {
  constructor() {
    this.currentLang = 'en';
    this.currentRole = 'FRONT_LINE';
    this.activeTab = 'frontline';
    this.currentStepIndex = 5; // Start at REFERRAL_REQUIRED
    this.isOffline = false;
    this.offlineQueue = [];
    this.simulationLog = [];

    this.init();
  }

  init() {
    this.render();
  }

  setLang(lang) {
    this.currentLang = lang;
    this.render();
  }

  setTab(tab) {
    this.activeTab = tab;
    this.render();
  }

  advanceStep() {
    if (this.currentStepIndex < CARE_STEPS.length - 1) {
      this.currentStepIndex++;
      const step = CARE_STEPS[this.currentStepIndex];
      this.logSim(`Transitioned journey to state: ${step.id} (${step.label})`);
      this.render();
    }
  }

  resetStep() {
    this.currentStepIndex = 0;
    this.logSim("Reset care journey to initial state: NEW");
    this.render();
  }

  simulateRejection() {
    this.logSim("[SIMULATED EVENT] Referral rejected by Pennagaram Taluk Hospital (ICU Bed Full) -> State machine safely maintained REFERRAL_REQUIRED and rerouted destination to Dharmapuri GMC Hospital.");
    alert("Referral Rejection Captured! State machine safely maintained REFERRAL_REQUIRED and rerouted destination.");
    this.render();
  }

  simulateOffline() {
    this.isOffline = !this.isOffline;
    if (this.isOffline) {
      this.offlineQueue.push({ id: `EVT-${Date.now()}`, type: "BP_MEASUREMENT", payload: "156/94 mmHg" });
      this.logSim("[OFFLINE MODE] Device disconnected from network. 1 clinical event queued to local encrypted storage.");
    } else {
      const count = this.offlineQueue.length;
      this.offlineQueue = [];
      this.logSim(`[RECONNECT SYNC] Reconnected to server. Synced ${count} events with server with 0 duplicate collisions.`);
    }
    this.render();
  }

  logSim(msg) {
    const time = new Date().toLocaleTimeString();
    this.simulationLog.unshift(`[${time}] ${msg}`);
    if (this.simulationLog.length > 8) this.simulationLog.pop();
  }

  render() {
    const t = I18N[this.currentLang];
    const root = document.getElementById('app-root');

    root.innerHTML = `
      <!-- Header -->
      <header class="header-bar">
        <div class="brand-section">
          <div class="logo-icon">C+</div>
          <div>
            <div class="brand-title">${t.appTitle}</div>
            <div class="brand-subtitle">${t.subtitle}</div>
          </div>
        </div>
        <div class="nav-controls">
          <select class="lang-selector" onchange="window.app.setLang(this.value)">
            <option value="en" ${this.currentLang === 'en' ? 'selected' : ''}>English</option>
            <option value="ta" ${this.currentLang === 'ta' ? 'selected' : ''}>தமிழ் (Tamil)</option>
            <option value="hi" ${this.currentLang === 'hi' ? 'selected' : ''}>हिंदी (Hindi)</option>
            <option value="mr" ${this.currentLang === 'mr' ? 'selected' : ''}>मराठी (Marathi)</option>
          </select>
          <div class="provenance-badge ${this.isOffline ? 'badge-stale' : 'badge-verified'}">
            ${this.isOffline ? '⚡ OFFLINE MODE (Local Queue)' : '● [SIMULATED DOUBLE] Testbed Mode'}
          </div>
        </div>
      </header>

      <!-- Tab Navigation -->
      <nav class="tab-navigation">
        <button class="tab-btn ${this.activeTab === 'frontline' ? 'active' : ''}" onclick="window.app.setTab('frontline')">👩‍⚕️ ${t.tabFrontline}</button>
        <button class="tab-btn ${this.activeTab === 'doctor' ? 'active' : ''}" onclick="window.app.setTab('doctor')">🩺 ${t.tabDoctor}</button>
        <button class="tab-btn ${this.activeTab === 'referral' ? 'active' : ''}" onclick="window.app.setTab('referral')">📋 ${t.tabReferral}</button>
        <button class="tab-btn ${this.activeTab === 'patient' ? 'active' : ''}" onclick="window.app.setTab('patient')">👤 ${t.tabPatient}</button>
        <button class="tab-btn ${this.activeTab === 'command' ? 'active' : ''}" onclick="window.app.setTab('command')">📊 ${t.tabCommand}</button>
        <button class="tab-btn ${this.activeTab === 'integrations' ? 'active' : ''}" onclick="window.app.setTab('integrations')">🔌 ${t.tabIntegrations}</button>
        <button class="tab-btn ${this.activeTab === 'simulation' ? 'active' : ''}" onclick="window.app.setTab('simulation')">⚙️ ${t.tabSimulation}</button>
      </nav>

      <!-- Main Body -->
      <main class="main-content">
        <!-- 14-Stage Care Journey Rail -->
        <div class="journey-banner">
          <div class="journey-header">
            <div class="patient-info-block">
              <div class="patient-avatar">MR</div>
              <div>
                <div class="patient-name">${t.patientName}</div>
                <div class="patient-meta">${t.patientMeta}</div>
              </div>
            </div>
            <div>
              <span class="provenance-badge badge-verified">State: ${CARE_STEPS[this.currentStepIndex].id}</span>
              <span class="provenance-badge badge-verified" style="margin-left:8px;">[SIMULATED] Freshness: Class A</span>
            </div>
          </div>

          <div class="steps-rail">
            ${CARE_STEPS.map((step, idx) => {
              const isCompleted = idx < this.currentStepIndex;
              const isActive = idx === this.currentStepIndex;
              return `
                <div class="step-node ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}">
                  <div class="step-circle">${isCompleted ? '✓' : idx + 1}</div>
                  <div class="step-label">${step.label}</div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Dynamic Tab View -->
        ${this.renderActiveView(t)}
      </main>
    `;
  }

  renderActiveView(t) {
    if (this.activeTab === 'frontline') {
      return `
        <div class="dashboard-grid">
          <div class="card">
            <div class="card-header">
              <div class="card-title">🚨 Prioritized Action Inbox</div>
              <span class="provenance-badge badge-critical">1 High Risk</span>
            </div>
            <p style="font-size:14px; color:var(--text-muted); margin-bottom:12px;">
              <strong>Meenakshi Ramasamy</strong> (BP: 168/104 mmHg • ECG: ST Depression). Referral required to District Hospital.
            </p>
            <div class="provenance-badge badge-verified" style="margin-bottom:14px;">
              [SIMULATED] Source: TN_MTM_PORTAL • Class C Batch Data
            </div>
            <div style="display:flex; gap:10px;">
              <button class="btn-primary" onclick="window.app.advanceStep()">Initiate Referral</button>
              <button class="btn-secondary" onclick="window.app.simulateOffline()">Toggle Offline Mode</button>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <div class="card-title">🤖 Explainable Facility Recommendations</div>
              <span class="provenance-badge badge-verified">[SIMULATED] Freshness: 94%</span>
            </div>
            <div style="font-size:13px; line-height:1.6;">
              <div style="background:rgba(56,189,248,0.1); border-left:3px solid var(--primary-blue); padding:10px; border-radius:4px; margin-bottom:10px;">
                <strong>1. Dharmapuri Govt Medical College Hospital (Rank #1)</strong><br/>
                <span style="color:var(--text-muted);">• Cardiology & ECG verified available (4 min ago)</span><br/>
                <span style="color:var(--text-muted);">• Distance: 18.5 km • 108 Corridor Feasible</span><br/>
                <span style="color:var(--text-muted);">• Scheme Empaneled: CMCHIS / PM-JAY</span>
              </div>
              <div style="background:rgba(255,255,255,0.03); border-left:3px solid var(--warning-amber); padding:10px; border-radius:4px;">
                <strong>2. Pennagaram Taluk Hospital (Rank #2)</strong><br/>
                <span style="color:var(--warning-amber);">• ICU at 95% capacity • [SIMULATED] Stale Telemetry (18m ago)</span><br/>
                <span style="color:var(--text-muted);">• Action: Frontline telephone confirmation required</span>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    if (this.activeTab === 'doctor') {
      return `
        <div class="dashboard-grid">
          <div class="card">
            <div class="card-header">
              <div class="card-title">🩺 Clinical Case Summary (ABDM FHIR Bundle)</div>
              <span class="provenance-badge badge-verified">[SIMULATED] ABDM IG 6.5.0 Aligned</span>
            </div>
            <div class="code-box">
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    { "resourceType": "Condition", "code": "I10 Essential Hypertension" },
    { "resourceType": "Observation", "code": "BP 168/104 mmHg", "status": "final" },
    { "resourceType": "DiagnosticReport", "code": "ECG ST-T Changes", "conclusion": "Ischemia" }
  ]
}
            </div>
            <div style="margin-top:16px; display:flex; gap:10px;">
              <button class="btn-primary" onclick="window.app.advanceStep()">Accept Referral & Confirm Admission</button>
            </div>
          </div>

          <div class="card">
            <div class="card-header">
              <div class="card-title">💊 Pharmacy & Drug Availability (DVDMS)</div>
              <span class="provenance-badge badge-verified">[SIMULATED] Updated 11m ago</span>
            </div>
            <p style="font-size:14px; margin-bottom:8px;"><strong>Amlodipine 5mg:</strong> 450 units available (In Stock)</p>
            <p style="font-size:14px; margin-bottom:8px;"><strong>Telmisartan 40mg:</strong> 320 units available (In Stock)</p>
            <div class="provenance-badge badge-stale" style="margin-top:10px;">
              [SIMULATED] Atorvastatin: Availability cannot be confirmed (Last verified 42m ago). Action: Call pharmacy.
            </div>
          </div>
        </div>
      `;
    }

    if (this.activeTab === 'referral') {
      return `
        <div class="dashboard-grid">
          <div class="card">
            <div class="card-header">
              <div class="card-title">📋 Referral Queue & 108 Transport Link</div>
              <span class="provenance-badge badge-verified">[SIMULATED] Live GPS Mode</span>
            </div>
            <p style="font-size:14px; margin-bottom:6px;"><strong>Vehicle TN-29-G-1084:</strong> En Route to Patient Pickup</p>
            <p style="font-size:14px; margin-bottom:6px;"><strong>GPS Status:</strong> 6.8 km away • ETA 14 mins (Simulated feed updated 14s ago)</p>
            <div class="provenance-badge badge-verified" style="margin-top:10px;">
              Source: STATE_108_CAD_SYSTEM (Class A Real-Time Mode Double)
            </div>
            <div style="margin-top:16px;">
              <button class="btn-primary" onclick="window.app.advanceStep()">Mark Patient Arrived at Hospital</button>
            </div>
          </div>
        </div>
      `;
    }

    if (this.activeTab === 'patient') {
      return `
        <div class="card" style="max-width:700px; margin:0 auto;">
          <div class="card-header">
            <div class="card-title">👤 ${t.patientName} — ${t.nextAction}</div>
            <span class="provenance-badge badge-verified">Assisted Care</span>
          </div>
          <div style="background:rgba(56,189,248,0.12); padding:16px; border-radius:12px; margin-bottom:16px;">
            <h3 style="font-family:var(--font-heading); color:var(--primary-blue); margin-bottom:8px;">
              🏥 Appointment at Dharmapuri Govt Medical College Hospital
            </h3>
            <p style="font-size:14px;">Specialist: Dr. A. Sundaram, MD (Cardiology) • Slot: Tomorrow 10:00 AM</p>
            <p style="font-size:14px;">Ambulance 108 is booked for pickup at 09:00 AM from PHC Karimangalam.</p>
          </div>
          <p style="font-size:13px; color:var(--text-muted);">
            Scan QR token at receiving facility referral desk for instant priority check-in.
          </p>
        </div>
      `;
    }

    if (this.activeTab === 'command') {
      return `
        <div class="dashboard-grid">
          <div class="card">
            <div class="card-header">
              <div class="card-title">📊 District Operational Health Metrics</div>
              <span class="provenance-badge badge-verified">Dharmapuri Pilot Synthetic Model</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:14px;">
              <div style="background:rgba(255,255,255,0.04); padding:12px; border-radius:8px;">
                <div style="font-size:24px; font-weight:800; color:var(--primary-blue);">88.4%</div>
                <div style="font-size:12px; color:var(--text-muted);">Target Referral Closure Rate</div>
              </div>
              <div style="background:rgba(255,255,255,0.04); padding:12px; border-radius:8px;">
                <div style="font-size:24px; font-weight:800; color:var(--verified-emerald);">2.4 days</div>
                <div style="font-size:12px; color:var(--text-muted);">Target Time to Consult</div>
              </div>
            </div>
            <p style="font-size:13px; color:var(--text-muted);">
              Note: Baseline measurements in progress. Impact claims will be reported post-pilot evaluation.
            </p>
          </div>

          <div class="card">
            <div class="card-header">
              <div class="card-title">🗺️ Rural Health Equity Disparity Index</div>
              <span class="provenance-badge badge-critical">Intervention Recommended</span>
            </div>
            <p style="font-size:13px; margin-bottom:8px;">
              <strong>Pennagaram Forest Block:</strong> Disparity Score 0.68 (Critical) • Recommends +1 MMU deployment.
            </p>
            <p style="font-size:13px; margin-bottom:8px;">
              <strong>Harur Tribal Border:</strong> Disparity Score 0.52 (Elevated) • Bi-weekly specialist tele-camps scheduled.
            </p>
          </div>
        </div>
      `;
    }

    if (this.activeTab === 'integrations') {
      return `
        <div class="card">
          <div class="card-header">
            <div class="card-title">🔌 Integration Reality & Maturity Ledger</div>
            <span class="provenance-badge badge-verified">7 Subsystems Monitored</span>
          </div>
          <p style="font-size:13px; color:var(--text-muted); margin-bottom:16px;">
            Unvarnished status distinguishing local automated double verification from external government production authorization.
          </p>
          <div style="display:flex; flex-direction:column; gap:10px;">
            ${INTEGRATIONS.map(i => `
              <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); padding:12px 16px; border-radius:8px; border:1px solid var(--border-color);">
                <div>
                  <strong style="font-size:14px;">${i.name}</strong>
                  <div style="font-size:12px; color:var(--text-muted);">${i.status} • ${i.freshness}</div>
                </div>
                <div class="provenance-badge badge-verified">${i.maturity}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    if (this.activeTab === 'simulation') {
      return `
        <div class="sim-panel">
          <div class="card-title" style="color:var(--primary-blue);">⚙️ Care Journey Interactive Simulation Console</div>
          <p style="font-size:13px; color:var(--text-muted); margin-top:4px;">
            Simulate happy path transitions, referral rejection/rerouting, offline field sync, and recovery.
          </p>

          <div class="sim-btn-group">
            <button class="btn-primary" onclick="window.app.advanceStep()">▶️ Advance Next Step (${CARE_STEPS[Math.min(this.currentStepIndex + 1, CARE_STEPS.length - 1)].label})</button>
            <button class="btn-secondary" onclick="window.app.simulateRejection()">⚠️ Simulate Referral Rejection & Rerouting</button>
            <button class="btn-secondary" onclick="window.app.simulateOffline()">⚡ Simulate Offline Queue & Replay</button>
            <button class="btn-secondary" onclick="window.app.resetStep()">🔄 Reset Journey to Start</button>
          </div>

          <div style="margin-top:16px;">
            <div style="font-size:12px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">LIVE SIMULATION EVENT LEDGER:</div>
            <div class="code-box" style="min-height:120px;">
              ${this.simulationLog.length ? this.simulationLog.join('<br/>') : 'Ready for simulation. Click any action above.'}
            </div>
          </div>
        </div>
      `;
    }
  }
}

// Initialize globally
window.onload = () => {
  window.app = new CareFlowApp();
};
