from datetime import datetime,timedelta
from fastapi import FastAPI,Depends,HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select
from .db import init_db,get_db
from .models import *
from pydantic import BaseModel

app=FastAPI(title='CareFlow Orchestration API',version='0.1.0')
@app.on_event('startup')
def startup(): init_db()
@app.get('/api/health')
def health(): return {'status':'UP','mode':'prototype'}
@app.get('/api/patients')
def patients(db:Session=Depends(get_db)): return db.scalars(select(Patient).order_by(Patient.created_at.desc())).all()
@app.get('/api/demo')
def demo(db:Session=Depends(get_db)):
    p=db.scalar(select(Patient).where(Patient.display_name=='Meenakshi R.')); 
    if not p: raise HTTPException(404,'Run seed first')
    j=db.scalar(select(CareJourney).where(CareJourney.patient_id==p.id)); r=db.scalar(select(Referral).where(Referral.journey_id==j.id))
    return {'journey_id':j.id,'referral_id':r.id}
@app.get('/api/journeys/{jid}')
def journey(jid:str,db:Session=Depends(get_db)):
    j=db.get(CareJourney,jid)
    if not j: raise HTTPException(404,'Journey not found')
    ev=db.scalars(select(JourneyEvent).where(JourneyEvent.journey_id==jid).order_by(JourneyEvent.occurred_at)).all()
    return {'journey':j,'events':ev}
@app.post('/api/referrals/{rid}/accept')
def accept(rid:str,db:Session=Depends(get_db)):
    r=db.get(Referral,rid)
    if not r: raise HTTPException(404,'Referral not found')
    r.status='ACCEPTED'; j=db.get(CareJourney,r.journey_id)
    if j.state!=JourneyState.REFERRAL_REQUIRED.value: raise HTTPException(400,'Journey is not awaiting referral acceptance')
    j.state=JourneyState.REFERRAL_ACCEPTED.value
    db.add(JourneyEvent(journey_id=j.id,event_type='ReferralAccepted',actor_ref='demo-referral-desk',source_system='FACILITY',payload={'referral_id':rid}))
    db.add(AuditEvent(actor_ref='demo-referral-desk',action='STATE_TRANSITION',resource_type='Referral',resource_id=rid,reason='Referral accepted'))
    db.commit(); db.refresh(r); return r
@app.get('/api/facilities/search')
def facilities(required:str,db:Session=Depends(get_db)):
    req={x.strip() for x in required.split(',') if x.strip()}
    rows=db.scalars(select(FacilityCapability).where(FacilityCapability.status=='AVAILABLE')).all()
    grouped={}
    for x in rows: grouped.setdefault(x.facility_id,[]).append(x)
    out=[]
    for fid,items in grouped.items():
        caps={x.capability for x in items}; match=len(req&caps)/max(1,len(req)); dist=min(x.distance_km for x in items); score=round(75*match+max(0,25-dist*.25),1)
        out.append({'facility_id':fid,'facility_name':items[0].facility_name,'score':score,'capabilities':sorted(caps),'distance_km':dist,'availability_note':items[0].availability_note,'verified_at':max(x.verified_at for x in items)})
    return sorted(out,key=lambda x:x['score'],reverse=True)
@app.post('/api/referrals/{rid}/appointment')
def appointment(rid:str,facility_ref:str,db:Session=Depends(get_db)):
    r=db.get(Referral,rid)
    if not r: raise HTTPException(404,'Referral not found')
    r.destination_facility=facility_ref; r.status='SCHEDULED'; now=datetime.utcnow(); a=Appointment(referral_id=rid,facility_ref=facility_ref,provider_ref='demo-specialist',slot_start=now+timedelta(hours=4),slot_end=now+timedelta(hours=4,minutes=30)); db.add(a)
    j=db.get(CareJourney,r.journey_id)
    if j.state==JourneyState.REFERRAL_ACCEPTED.value: j.state=JourneyState.APPOINTMENT_CONFIRMED.value; db.add(JourneyEvent(journey_id=j.id,event_type='AppointmentConfirmed',actor_ref='demo-referral-desk',source_system='UHI',payload={'appointment_id':a.id,'facility_id':facility_ref}))
    db.commit(); return {'referral':r,'appointment':a}
class ExternalEvent(BaseModel): event_id:str; source_system:str; journey_id:str; event_type:str; actor_ref:str|None=None; payload:dict={}
@app.post('/api/events')
def event(req:ExternalEvent,db:Session=Depends(get_db)):
    old=db.scalar(select(IntegrationMessage).where(IntegrationMessage.source_system==req.source_system,IntegrationMessage.idempotency_key==req.event_id))
    if old: return {'status':'DUPLICATE_IGNORED','message_id':old.id}
    m=IntegrationMessage(source_system=req.source_system,idempotency_key=req.event_id); db.add(m); db.commit(); return {'status':'ACCEPTED','message_id':m.id}
app.mount('/',StaticFiles(directory='app/static',html=True),name='static')
