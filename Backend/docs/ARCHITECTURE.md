# Backend architecture notes

## Core rule

External systems own domain records. CareFlow owns operational journey state.

## Transaction boundary

A journey transition and its JourneyEvent + AuditEvent + OutboxEvent should be committed in one database transaction.

## Idempotency

Every inbound external event must carry:
- source_system
- idempotency_key / event_id
- payload hash
- occurred_at

The integration_messages unique constraint prevents duplicate application.

## Event publication

Use the transactional outbox pattern. Business transaction writes the outbox row; a worker publishes it to Kafka/RabbitMQ. Never publish directly inside the HTTP transaction.

## Facility matching

Keep operational capability snapshots separate from HFR identity. Every capability must have source_system + last_verified_at.

## Offline sync

Mobile clients generate stable EventID values. Retried events produce the same EventID and/or Idempotency-Key.

## Clinical safety

Clinical transitions are performed by authorized users. AI may recommend; a human commits the patient-impacting transition.
