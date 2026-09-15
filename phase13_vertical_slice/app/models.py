from datetime import datetime
from enum import Enum
from uuid import uuid4
from sqlalchemy import String, DateTime, ForeignKey, Text, Integer, JSON, UniqueConstraint, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

def uid(): return str(uuid4())
class Base(DeclarativeBase): pass
class JourneyState(str, Enum):
    NEW='NEW'; TRIAGED='TRIAGED'; CONSULTATION_REQUIRED='CONSULTATION_REQUIRED'; CONSULTED='CONSULTED'
    DIAGNOSTIC_REQUIRED='DIAGNOSTIC_REQUIRED'; DIAGNOSTIC_IN_PROGRESS='DIAGNOSTIC_IN_PROGRESS'; DIAGNOSTIC_COMPLETED='DIAGNOSTIC_COMPLETED'
    REFERRAL_REQUIRED='REFERRAL_REQUIRED'; REFERRAL_ACCEPTED='REFERRAL_ACCEPTED'; APPOINTMENT_CONFIRMED='APPOINTMENT_CONFIRMED'
    TRANSPORT_CONFIRMED='TRANSPORT_CONFIRMED'; PATIENT_ARRIVED='PATIENT_ARRIVED'; TREATMENT_COMPLETED='TREATMENT_COMPLETED'
    MEDICINE_FULFILLED='MEDICINE_FULFILLED'; FOLLOW_UP_ACTIVE='FOLLOW_UP_ACTIVE'; CLOSED='CLOSED'
ALLOWED={
JourneyState.NEW:{JourneyState.TRIAGED}, JourneyState.TRIAGED:{JourneyState.CONSULTATION_REQUIRED,JourneyState.CONSULTED},
JourneyState.CONSULTATION_REQUIRED:{JourneyState.CONSULTED}, JourneyState.CONSULTED:{JourneyState.DIAGNOSTIC_REQUIRED,JourneyState.REFERRAL_REQUIRED},
JourneyState.DIAGNOSTIC_REQUIRED:{JourneyState.DIAGNOSTIC_IN_PROGRESS}, JourneyState.DIAGNOSTIC_IN_PROGRESS:{JourneyState.DIAGNOSTIC_COMPLETED},
JourneyState.DIAGNOSTIC_COMPLETED:{JourneyState.REFERRAL_REQUIRED,JourneyState.FOLLOW_UP_ACTIVE}, JourneyState.REFERRAL_REQUIRED:{JourneyState.REFERRAL_ACCEPTED},
JourneyState.REFERRAL_ACCEPTED:{JourneyState.APPOINTMENT_CONFIRMED}, JourneyState.APPOINTMENT_CONFIRMED:{JourneyState.TRANSPORT_CONFIRMED,JourneyState.PATIENT_ARRIVED},
JourneyState.TRANSPORT_CONFIRMED:{JourneyState.PATIENT_ARRIVED}, JourneyState.PATIENT_ARRIVED:{JourneyState.TREATMENT_COMPLETED},
JourneyState.TREATMENT_COMPLETED:{JourneyState.MEDICINE_FULFILLED,JourneyState.FOLLOW_UP_ACTIVE}, JourneyState.MEDICINE_FULFILLED:{JourneyState.FOLLOW_UP_ACTIVE},
JourneyState.FOLLOW_UP_ACTIVE:{JourneyState.CLOSED}}
class Patient(Base):
    __tablename__='patients'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); display_name:Mapped[str]=mapped_column(String(200)); abha_ref:Mapped[str|None]=mapped_column(String(120)); status:Mapped[str]=mapped_column(String(30),default='ACTIVE'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class CareJourney(Base):
    __tablename__='care_journeys'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); patient_id:Mapped[str]=mapped_column(ForeignKey('patients.id')); pathway:Mapped[str]=mapped_column(String(80)); state:Mapped[str]=mapped_column(String(50),default='NEW'); priority:Mapped[str]=mapped_column(String(20),default='ROUTINE'); owner_ref:Mapped[str|None]=mapped_column(String(160)); opened_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); closed_at:Mapped[datetime|None]=mapped_column(DateTime)
class JourneyEvent(Base):
    __tablename__='journey_events'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); journey_id:Mapped[str]=mapped_column(ForeignKey('care_journeys.id')); event_type:Mapped[str]=mapped_column(String(100)); actor_ref:Mapped[str|None]=mapped_column(String(160)); source_system:Mapped[str|None]=mapped_column(String(100)); occurred_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); payload:Mapped[dict]=mapped_column(JSON,default=dict)
class Referral(Base):
    __tablename__='referrals'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); journey_id:Mapped[str]=mapped_column(ForeignKey('care_journeys.id')); source_facility:Mapped[str]=mapped_column(String(160)); destination_facility:Mapped[str|None]=mapped_column(String(160)); reason:Mapped[str]=mapped_column(Text); urgency:Mapped[str]=mapped_column(String(20),default='ROUTINE'); status:Mapped[str]=mapped_column(String(40),default='CREATED'); due_at:Mapped[datetime|None]=mapped_column(DateTime); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Appointment(Base):
    __tablename__='appointments'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); referral_id:Mapped[str]=mapped_column(ForeignKey('referrals.id')); facility_ref:Mapped[str]=mapped_column(String(160)); provider_ref:Mapped[str|None]=mapped_column(String(160)); slot_start:Mapped[datetime]=mapped_column(DateTime); slot_end:Mapped[datetime]=mapped_column(DateTime); status:Mapped[str]=mapped_column(String(40),default='CONFIRMED')
class Task(Base):
    __tablename__='tasks'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); journey_id:Mapped[str]=mapped_column(ForeignKey('care_journeys.id')); task_type:Mapped[str]=mapped_column(String(80)); owner_ref:Mapped[str|None]=mapped_column(String(160)); priority:Mapped[str]=mapped_column(String(20),default='ROUTINE'); status:Mapped[str]=mapped_column(String(40),default='OPEN'); due_at:Mapped[datetime|None]=mapped_column(DateTime)
class FacilityCapability(Base):
    __tablename__='facility_capabilities'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); facility_id:Mapped[str]=mapped_column(String(160)); facility_name:Mapped[str]=mapped_column(String(200)); capability:Mapped[str]=mapped_column(String(120)); status:Mapped[str]=mapped_column(String(30),default='AVAILABLE'); distance_km:Mapped[float]=mapped_column(Float); availability_note:Mapped[str]=mapped_column(String(200)); verified_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class AuditEvent(Base):
    __tablename__='audit_events'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); actor_ref:Mapped[str|None]=mapped_column(String(160)); action:Mapped[str]=mapped_column(String(100)); resource_type:Mapped[str]=mapped_column(String(80)); resource_id:Mapped[str|None]=mapped_column(String(160)); reason:Mapped[str|None]=mapped_column(Text); occurred_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class IntegrationMessage(Base):
    __tablename__='integration_messages'; id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); source_system:Mapped[str]=mapped_column(String(100)); idempotency_key:Mapped[str]=mapped_column(String(160)); payload_hash:Mapped[str|None]=mapped_column(String(128)); status:Mapped[str]=mapped_column(String(30),default='RECEIVED'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); __table_args__=(UniqueConstraint('source_system','idempotency_key'),)
