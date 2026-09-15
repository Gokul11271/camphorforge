INSERT INTO patients (patient_ref, display_name, abha_ref)
VALUES ('7b6e56c4-71e1-4e6b-9c34-3a1a0e6a0f21', 'Meenakshi R.', 'DEMO-ABHA-281');

INSERT INTO care_journeys (journey_id, patient_ref, pathway, state, priority, owner_user_ref)
VALUES (
 '8aa8eb7d-e1c3-4667-9d18-4a1e2e7c1289',
 '7b6e56c4-71e1-4e6b-9c34-3a1a0e6a0f21',
 'NCD_REFERRAL',
 'REFERRAL_REQUIRED',
 'HIGH',
 'demo-cho-001'
);

INSERT INTO referrals (referral_id, journey_id, source_facility_ref, destination_facility_ref, reason, urgency, status, due_at)
VALUES (
 '3f9c2a55-2bca-4f9f-8dc4-8c78de5a9e44',
 '8aa8eb7d-e1c3-4667-9d18-4a1e2e7c1289',
 'TN-PHC-CLUSTER-03',
 'TN-DH-DEMO',
 'Persistent uncontrolled diabetes; medicine specialist review',
 'HIGH',
 'CREATED',
 now() + interval '6 hours'
);
