# Phase 13 — Working Vertical Slice

Local full-stack prototype for the Rural Healthcare Care-Orchestration Platform.

## Implemented
- FastAPI backend
- SQLite development DB (PostgreSQL-compatible SQLAlchemy design)
- Patient, CareJourney, Referral, Task, FacilityCapability, JourneyEvent, AuditEvent
- Explicit care-state machine
- Referral acceptance and appointment attachment
- Facility capability ranking
- Idempotent external event ingestion
- Simple responsive browser UI connected to the API
- Dockerfile + Docker Compose

## Run
python -m venv .venv
pip install -r requirements.txt
python scripts/seed.py
uvicorn app.main:app --reload

Open http://127.0.0.1:8000
API docs: http://127.0.0.1:8000/docs

This prototype uses synthetic data only. It is not connected to live ABDM/UHI/eSanjeevani/state systems.
