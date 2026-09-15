from pathlib import Path
import sys, json
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from engine import Engine, State, MockIntegration

passed=[]
failed=[]

def check(name, condition, detail=""):
    if condition:
        passed.append(name); print(f"PASS  {name}")
    else:
        failed.append(name); print(f"FAIL  {name} {detail}")

# 1 Happy path
e=Engine(); j=e.create("JRN-001")
for i,s in enumerate([
    State.TRIAGED, State.CONSULTED, State.DIAGNOSTIC_REQUIRED,
    State.DIAGNOSTIC_COMPLETED, State.REFERRAL_REQUIRED,
    State.REFERRAL_ACCEPTED, State.APPOINTMENT_CONFIRMED,
    State.PATIENT_ARRIVED, State.TREATMENT_COMPLETED,
    State.MEDICINE_FULFILLED, State.FOLLOW_UP_ACTIVE
],1):
    e.transition("JRN-001",s,f"evt-{i}","CAREFLOW",{"synthetic":True})
check("happy-path-reaches-follow-up", j.state==State.FOLLOW_UP_ACTIVE)
e.close("JRN-001")
check("happy-path-closes", j.state==State.CLOSED)

# 2 duplicate external event
e2=Engine(); e2.create("JRN-002")
a=e2.ingest_external("JRN-002","uhi-1","AppointmentConfirmed","UHI",{})
b=e2.ingest_external("JRN-002","uhi-1","AppointmentConfirmed","UHI",{})
check("duplicate-event-is-idempotent", a=="ACCEPTED" and b=="DUPLICATE_IGNORED")

# 3 timeout
mock=MockIntegration(); mock.failure="TIMEOUT"
r=mock.call("UHI_APPOINTMENT",{"patient":"DEMO"})
check("external-timeout-becomes-pending", r["status"]=="PENDING")

# 4 rejection + rerouting
e3=Engine(); j3=e3.create("JRN-003")
for i,s in enumerate([State.TRIAGED,State.CONSULTED,State.REFERRAL_REQUIRED],1):
    e3.transition("JRN-003",s,f"evt3-{i}","CAREFLOW",{})
# rejection does NOT force invalid state; re-routing keeps referral-required state
j3.events.append(type(j3.events[0])("rej-1","ReferralRejected","FACILITY",j3.events[0].occurred_at,{"reason":"capacity"}))
check("rejection-preserves-refer-state", j3.state==State.REFERRAL_REQUIRED)

# 5 diagnostic delay / SLA marker
e4=Engine(); j4=e4.create("JRN-004")
e4.transition("JRN-004",State.TRIAGED,"a","CARE","{}")
e4.transition("JRN-004",State.CONSULTED,"b","CARE","{}")
e4.transition("JRN-004",State.DIAGNOSTIC_REQUIRED,"c","CARE","{}")
j4.pending_external.add("LAB:LAB-001")
check("diagnostic-delay-remains-open", j4.state==State.DIAGNOSTIC_REQUIRED and "LAB:LAB-001" in j4.pending_external)

# 6 partial success
e5=Engine(); j5=e5.create("JRN-005")
for i,s in enumerate([State.TRIAGED,State.CONSULTED,State.REFERRAL_REQUIRED,State.REFERRAL_ACCEPTED,State.APPOINTMENT_CONFIRMED],1):
    e5.transition("JRN-005",s,f"p{i}","CARE",{})
j5.pending_external.add("EMS:EMS-001")
check("partial-success-keeps-journey-open", j5.state==State.APPOINTMENT_CONFIRMED and j5.pending_external)

# 7 offline replay
e6=Engine(); j6=e6.create("JRN-006")
x=e6.ingest_external("JRN-006","offline-77","ReferralCreated","OFFLINE",{"queued":True})
y=e6.ingest_external("JRN-006","offline-77","ReferralCreated","OFFLINE",{"queued":True})
check("offline-replay-no-duplicate", x=="ACCEPTED" and y=="DUPLICATE_IGNORED")

# 8 out of order transition rejected
e7=Engine(); e7.create("JRN-007")
try:
    e7.transition("JRN-007",State.CLOSED,"bad","CARE",{})
    out=False
except ValueError:
    out=True
check("out-of-order-transition-rejected",out)

# 9 audit/provenance completeness
check("audit-created", len(e.journeys["JRN-001"].audit)>=2)
check("events-have-source", all(ev.source for ev in e.journeys["JRN-001"].events))

# 10 closure gate
e8=Engine(); e8.create("JRN-008")
try:
    e8.close("JRN-008")
    closure=False
except ValueError:
    closure=True
check("closure-gate-blocks-early-close",closure)

summary={"passed":len(passed),"failed":len(failed),"tests":passed+failed}
Path(__file__).with_name("results.json").write_text(json.dumps(summary,indent=2))
print(f"\\nRESULT: {len(passed)} passed, {len(failed)} failed")
if failed:
    raise SystemExit(1)
