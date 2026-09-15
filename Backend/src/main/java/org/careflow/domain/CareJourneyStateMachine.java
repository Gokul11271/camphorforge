package org.careflow.domain;

import java.util.Map;
import java.util.Set;

public final class CareJourneyStateMachine {
    private static final Map<CareJourneyState, Set<CareJourneyState>> ALLOWED = Map.ofEntries(
        Map.entry(CareJourneyState.NEW, Set.of(CareJourneyState.TRIAGED)),
        Map.entry(CareJourneyState.TRIAGED, Set.of(CareJourneyState.CONSULTATION_REQUIRED, CareJourneyState.CONSULTED)),
        Map.entry(CareJourneyState.CONSULTATION_REQUIRED, Set.of(CareJourneyState.CONSULTED)),
        Map.entry(CareJourneyState.CONSULTED, Set.of(CareJourneyState.DIAGNOSTIC_REQUIRED, CareJourneyState.REFERRAL_REQUIRED, CareJourneyState.FOLLOW_UP_ACTIVE)),
        Map.entry(CareJourneyState.DIAGNOSTIC_REQUIRED, Set.of(CareJourneyState.DIAGNOSTIC_IN_PROGRESS, CareJourneyState.DIAGNOSTIC_COMPLETED)),
        Map.entry(CareJourneyState.DIAGNOSTIC_IN_PROGRESS, Set.of(CareJourneyState.DIAGNOSTIC_COMPLETED)),
        Map.entry(CareJourneyState.DIAGNOSTIC_COMPLETED, Set.of(CareJourneyState.REFERRAL_REQUIRED, CareJourneyState.FOLLOW_UP_ACTIVE, CareJourneyState.TREATMENT_COMPLETED)),
        Map.entry(CareJourneyState.REFERRAL_REQUIRED, Set.of(CareJourneyState.REFERRAL_ACCEPTED, CareJourneyState.REFERRAL_REQUIRED)),
        Map.entry(CareJourneyState.REFERRAL_ACCEPTED, Set.of(CareJourneyState.APPOINTMENT_CONFIRMED)),
        Map.entry(CareJourneyState.APPOINTMENT_CONFIRMED, Set.of(CareJourneyState.TRANSPORT_CONFIRMED, CareJourneyState.PATIENT_ARRIVED)),
        Map.entry(CareJourneyState.TRANSPORT_CONFIRMED, Set.of(CareJourneyState.PATIENT_ARRIVED)),
        Map.entry(CareJourneyState.PATIENT_ARRIVED, Set.of(CareJourneyState.TREATMENT_COMPLETED)),
        Map.entry(CareJourneyState.TREATMENT_COMPLETED, Set.of(CareJourneyState.MEDICINE_FULFILLED, CareJourneyState.FOLLOW_UP_ACTIVE)),
        Map.entry(CareJourneyState.MEDICINE_FULFILLED, Set.of(CareJourneyState.FOLLOW_UP_ACTIVE)),
        Map.entry(CareJourneyState.FOLLOW_UP_ACTIVE, Set.of(CareJourneyState.CLOSED))
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
