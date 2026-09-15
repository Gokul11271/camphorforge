# Phase 12 — Backend & Database Implementation Starter

Rural Care Access & Continuity Orchestration Platform

This starter implements the Phase 7/8 backend contract as a modular monolith with:
- Java 21 + Spring Boot structure
- PostgreSQL schema
- CareJourney state machine
- Referral/task/follow-up model
- Append-only journey events
- Idempotent external event ingestion
- Audit trail
- OpenAPI starter contract
- Docker Compose for PostgreSQL
- Synthetic demo data only

Important:
- This repository does NOT connect to live ABDM, UHI, eSanjeevani, NP-NCD, RCH, U-WIN, Nikshay, PM-JAY, state HMIS, LIS, LMIS or EMS.
- External integrations must be implemented behind adapters and authorized before production use.
- The schema intentionally stores references/provenance rather than becoming the source of truth for external clinical systems.

## Suggested local run

1. `docker compose up -d postgres`
2. `./mvnw spring-boot:run`
3. API: `http://localhost:8080`
4. Swagger/OpenAPI: `http://localhost:8080/swagger-ui/index.html` (when springdoc is enabled)

This scaffold is deliberately modular so the external adapter layer can be added without changing core business rules.
