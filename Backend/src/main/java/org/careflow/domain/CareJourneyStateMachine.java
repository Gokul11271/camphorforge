package org.careflow.domain;

import java.util.Map;
import java.util.Set;

public final class CareJourneyStateMachine {
    private static final Map<CareJourneyState, Set<CareJourneyState>> ALLOWED = Map.of(
        CareJourneyState.NEW, Set.of(CareJourneyState.TRIAGED),
        CareJourneyState.TRIAGED, Set.of(CareJourneyState.CONSULTATION_REQUIRED, CareJourneyState.CONSULTED),
        CareJourneyState.CONSULTATION_REQUIRED, Set.of(CareJourneyState.CONSULTED),
        CareJourneyState.CONSULTED, Set.of(CareJourneyState.DIAGNOSTIC_REQUIRED, CareJourneyState.REFERRAL_REQUIRED),
        CareJourneyState.DIAGNOSTIC_REQUIRED, Set.of(CareJourneyState.DIAGNOSTIC_IN_PROGRESS),
        CareJourneyState.DIAGNOSTIC_IN_PROGRESS, Set.of(CareJourneyState.DIAGNOSTIC_COMPLETED),
        CareJourneyState.DIAGNOSTIC_COMPLETED, Set.of(CareJourneyState.REFERRAL_REQUIRED, CareJourneyState.FOLLOW_UP_ACTIVE),
        CareJourneyState.REFERRAL_REQUIRED, Set.of(CareJourneyState.REFERRAL_ACCEPTED),
        CareJourneyState.REFERRAL_ACCEPTED, Set.of(CareJourneyState.APPOINTMENT_CONFIRMED),
        CareJourneyState.APPOINTMENT_CONFIRMED, Set.of(CareJourneyState.TRANSPORT_CONFIRMED, CareJourneyState.PATIENT_ARRIVED),
        CareJourneyState.TRANSPORT_CONFIRMED, Set.of(CareJourneyState.PATIENT_ARRIVED),
        CareJourneyState.PATIENT_ARRIVED, Set.of(CareJourneyState.TREATMENT_COMPLETED),
        CareJourneyState.TREATMENT_COMPLETED, Set.of(CareJourneyState.MEDICINE_FULFILLED, CareJourneyState.FOLLOW_UP_ACTIVE),
        CareJourneyState.MEDICINE_FULFILLED, Set.of(CareJourneyState.FOLLOW_UP_ACTIVE),
        CareJourneyState.FOLLOW_UP_ACTIVE, Set.of(CareJourneyState.CLOSED)
    );

    public static boolean canTransition(CareJourneyState from, CareJourneyState to) {
        return ALLOWED.getOrDefault(from, Set.of()).contains(to);
    }

    public static void assertTransition(CareJourneyState from, CareJourneyState to) {
        if (!canTransition(from, to)) {
            throw new IllegalStateException("Invalid care journey transition: " + from + " -> " + to);
        }
    }

    private CareJourneyStateMachine() {}
}
