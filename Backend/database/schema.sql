CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE patients (
    patient_ref UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
    display_name VARCHAR(200),
    abha_ref VARCHAR(120),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE patient_source_refs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_ref UUID NOT NULL REFERENCES patients(patient_ref),
    source_system VARCHAR(80) NOT NULL,
    source_id VARCHAR(160) NOT NULL,
    verified_at TIMESTAMPTZ,
    UNIQUE(source_system, source_id)
);

CREATE TABLE care_journeys (
    journey_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_ref UUID NOT NULL REFERENCES patients(patient_ref),
    pathway VARCHAR(60) NOT NULL,
    state VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL DEFAULT 'ROUTINE',
    owner_user_ref VARCHAR(120),
    opened_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    closed_at TIMESTAMPTZ
);

CREATE INDEX idx_care_journeys_patient ON care_journeys(patient_ref);
CREATE INDEX idx_care_journeys_state ON care_journeys(state, priority);

CREATE TABLE journey_events (
    event_id UUID PRIMARY KEY,
    journey_id UUID NOT NULL REFERENCES care_journeys(journey_id),
    type VARCHAR(80) NOT NULL,
    actor_ref VARCHAR(120),
    source_system VARCHAR(80),
    occurred_at TIMESTAMPTZ NOT NULL,
    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    payload_hash VARCHAR(128),
    UNIQUE(journey_id, event_id)
);

CREATE INDEX idx_journey_events_journey_time ON journey_events(journey_id, occurred_at);

CREATE TABLE referrals (
    referral_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id UUID NOT NULL REFERENCES care_journeys(journey_id),
    source_facility_ref VARCHAR(160) NOT NULL,
    destination_facility_ref VARCHAR(160),
    reason TEXT NOT NULL,
    urgency VARCHAR(20) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'CREATED',
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_referrals_status_due ON referrals(status, due_at);

CREATE TABLE appointments (
    appointment_ref UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referral_id UUID REFERENCES referrals(referral_id),
    provider_ref VARCHAR(160),
    facility_ref VARCHAR(160),
    slot_start TIMESTAMPTZ,
    slot_end TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'PENDING',
    source_system VARCHAR(80),
    external_id VARCHAR(160),
    UNIQUE(source_system, external_id)
);

CREATE TABLE diagnostic_orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id UUID NOT NULL REFERENCES care_journeys(journey_id),
    test_code VARCHAR(80) NOT NULL,
    facility_ref VARCHAR(160),
    status VARCHAR(40) NOT NULL DEFAULT 'ORDERED',
    ordered_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    source_system VARCHAR(80),
    external_id VARCHAR(160),
    UNIQUE(source_system, external_id)
);

CREATE TABLE diagnostic_results (
    result_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES diagnostic_orders(order_id),
    report_ref VARCHAR(200) NOT NULL,
    status VARCHAR(40) NOT NULL,
    issued_at TIMESTAMPTZ,
    source_system VARCHAR(80)
);

CREATE TABLE medication_plans (
    medication_plan_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id UUID NOT NULL REFERENCES care_journeys(journey_id),
    medication_code VARCHAR(120) NOT NULL,
    instructions TEXT,
    fulfilment_status VARCHAR(40) NOT NULL DEFAULT 'PENDING'
);

CREATE TABLE transport_requests (
    transport_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    referral_id UUID NOT NULL REFERENCES referrals(referral_id),
    mode VARCHAR(30),
    pickup TEXT,
    destination TEXT,
    status VARCHAR(40) NOT NULL DEFAULT 'REQUESTED',
    source_system VARCHAR(80),
    external_id VARCHAR(160),
    UNIQUE(source_system, external_id)
);

CREATE TABLE facility_capabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    facility_id VARCHAR(160) NOT NULL,
    capability_code VARCHAR(120) NOT NULL,
    status VARCHAR(30) NOT NULL,
    last_verified_at TIMESTAMPTZ,
    source_system VARCHAR(80),
    UNIQUE(facility_id, capability_code, source_system)
);

CREATE TABLE tasks (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id UUID REFERENCES care_journeys(journey_id),
    type VARCHAR(80) NOT NULL,
    owner_ref VARCHAR(160),
    priority VARCHAR(20) NOT NULL DEFAULT 'ROUTINE',
    due_at TIMESTAMPTZ,
    status VARCHAR(40) NOT NULL DEFAULT 'OPEN',
    escalation_level INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX idx_tasks_owner_status_due ON tasks(owner_ref, status, due_at);

CREATE TABLE followups (
    followup_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journey_id UUID NOT NULL REFERENCES care_journeys(journey_id),
    due_at TIMESTAMPTZ NOT NULL,
    owner_ref VARCHAR(160),
    type VARCHAR(80) NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'OPEN'
);

CREATE TABLE consent_contexts (
    consent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_ref UUID NOT NULL REFERENCES patients(patient_ref),
    purpose VARCHAR(160) NOT NULL,
    scope JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(30) NOT NULL,
    issued_at TIMESTAMPTZ,
    expiry_at TIMESTAMPTZ,
    source VARCHAR(100)
);

CREATE TABLE integration_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_system VARCHAR(80) NOT NULL,
    idempotency_key VARCHAR(160) NOT NULL,
    payload_hash VARCHAR(128),
    status VARCHAR(30) NOT NULL DEFAULT 'RECEIVED',
    retry_count INTEGER NOT NULL DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE(source_system, idempotency_key)
);

CREATE TABLE audit_events (
    audit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    actor_ref VARCHAR(160),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(80) NOT NULL,
    resource_id VARCHAR(160),
    reason TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(80) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at TIMESTAMPTZ
);

CREATE INDEX idx_outbox_unpublished ON outbox_events(published_at) WHERE published_at IS NULL;
