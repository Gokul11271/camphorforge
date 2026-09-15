# Phase 14 — Mock Government Integration Layer

This phase adds a production-shaped integration boundary around the CareFlow vertical slice.

Mock services:
- ABDM
- UHI
- eSanjeevani
- NP-NCD
- State HIS/LIS/LMIS
- EMS / 108 / 102

Important:
- All services are local mocks.
- No live government endpoint, credential, PHI or production patient data is used.
- Contracts are intentionally versioned.
- The internal CareFlow API should talk to adapters, never directly to vendor/government endpoints.
- Replace a mock adapter only after official onboarding, security review and state/program authorization.

## Files

`mock_integrations/server.py` provides FastAPI mock endpoints.

`mock_integrations/adapters.py` models the adapter contract used by the core.

`contracts/*.json` are sample request/response payloads.

`tests/test_contracts.py` validates core invariants.

## Run

Python 3.11+:

    pip install -r requirements.txt
    uvicorn mock_integrations.server:app --reload --port 9000

Mock API docs:
    http://127.0.0.1:9000/docs

Demo flow:
1. Create referral
2. UHI service search
3. Reserve appointment
4. eSanjeevani consultation
5. LIS diagnostic result
6. EMS transport request
7. Hospital arrival
8. PM/NCD follow-up signal

Use `curl` or Postman against localhost:9000.
