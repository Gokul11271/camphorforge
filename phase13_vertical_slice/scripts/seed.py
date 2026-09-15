from datetime import datetime,timedelta
from app.db import init_db,SessionLocal
from app.models import *
init_db(); db=SessionLocal()
if not db.scalar(__import__('sqlalchemy').select(Patient).where(Patient.display_name=='Meenakshi R.')):
    p=Patient(display_name='Meenakshi R.',abha_ref='DEMO-ABHA-281'); db.add(p); db.flush()
    j=CareJourney(patient_id=p.id,pathway='NCD_REFERRAL',state=JourneyState.REFERRAL_REQUIRED.value,priority='HIGH',owner_ref='demo-cho-001'); db.add(j); db.flush()
    db.add(Referral(journey_id=j.id,source_facility='TN-PHC-CLUSTER-03',destination_facility='TN-DH-DEMO',reason='Persistent uncontrolled diabetes; medicine specialist review',urgency='HIGH',status='CREATED',due_at=datetime.utcnow()+timedelta(hours=6)))
    db.add(JourneyEvent(journey_id=j.id,event_type='ScreeningCompleted',actor_ref='demo-cho-001',source_system='NP-NCD',payload={'demo':True}))
    db.add(JourneyEvent(journey_id=j.id,event_type='ConsultationCompleted',actor_ref='demo-doctor-001',source_system='eSanjeevani',payload={'demo':True}))
    for fid,name,cap,dist,note in [
        ('TN-DH-DEMO','District Hospital','Medicine',38,'Medicine specialist available; appointment today'),
        ('TN-DH-DEMO','District Hospital','HbA1c',38,'Diagnostic available'),
        ('TN-DH-DEMO','District Hospital','RenalFunction',38,'Diagnostic available'),
        ('TN-TH-DEMO','Taluk Hospital','Medicine',19,'Medicine specialist; diagnostic capacity limited'),
        ('TN-TH-DEMO','Taluk Hospital','HbA1c',19,'Limited diagnostic slots'),
        ('TN-MC-DEMO','Medical College','Medicine',52,'Specialist available; longer wait'),
        ('TN-MC-DEMO','Medical College','HbA1c',52,'Diagnostic available'),
        ('TN-MC-DEMO','Medical College','RenalFunction',52,'Diagnostic available')]: db.add(FacilityCapability(facility_id=fid,facility_name=name,capability=cap,distance_km=dist,availability_note=note))
    db.add(Task(journey_id=j.id,task_type='CONFIRM_REFERRAL',owner_ref='referral-desk',priority='HIGH',due_at=datetime.utcnow()+timedelta(hours=2))); db.commit()
print('seed complete')
