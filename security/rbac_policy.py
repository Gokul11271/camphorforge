"""
Role-Based and Attribute-Based Access Control (RBAC & ABAC) Policy Engine
Implements strict least-privilege access rules across 16 healthcare roles.
"""
from enum import Enum
from typing import Any, Optional


class HealthcareRole(str, Enum):
    PATIENT = "PATIENT"
    ASHA = "ASHA"
    ANM = "ANM"
    CHO = "CHO"
    NURSE = "NURSE"
    DOCTOR = "DOCTOR"
    SPECIALIST = "SPECIALIST"
    REFERRAL_COORDINATOR = "REFERRAL_COORDINATOR"
    LAB_USER = "LAB_USER"
    PHARMACY_USER = "PHARMACY_USER"
    TRANSPORT_OPERATOR = "TRANSPORT_OPERATOR"
    FACILITY_ADMIN = "FACILITY_ADMIN"
    DISTRICT_MANAGER = "DISTRICT_MANAGER"
    STATE_MANAGER = "STATE_MANAGER"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    AUDITOR = "AUDITOR"


# Permission definitions
PERMISSIONS_MATRIX: dict[HealthcareRole, set[str]] = {
    HealthcareRole.PATIENT: {
        "journey:read_own", "appointment:read_own", "consent:manage_own", "transport:read_own"
    },
    HealthcareRole.ASHA: {
        "journey:read_assigned", "journey:create", "triage:perform", "task:read_assigned",
        "task:update", "offline:sync", "transport:request"
    },
    HealthcareRole.ANM: {
        "journey:read_assigned", "journey:create", "triage:perform", "anc:update", "immunization:update",
        "task:read_assigned", "offline:sync"
    },
    HealthcareRole.CHO: {
        "journey:read_facility", "journey:create", "triage:perform", "referral:create",
        "diagnostic:order", "teleconsultation:initiate", "task:manage", "offline:sync"
    },
    HealthcareRole.DOCTOR: {
        "journey:read_all", "clinical:consult", "referral:create", "referral:accept",
        "diagnostic:order", "diagnostic:review", "medication:prescribe", "discharge:complete"
    },
    HealthcareRole.SPECIALIST: {
        "journey:read_all", "clinical:consult", "referral:accept", "diagnostic:order",
        "diagnostic:review", "medication:prescribe", "teleconsultation:conduct"
    },
    HealthcareRole.REFERRAL_COORDINATOR: {
        "referral:read_queue", "referral:accept", "referral:reroute", "appointment:book",
        "transport:link", "facility:query_capacity"
    },
    HealthcareRole.LAB_USER: {
        "diagnostic:read_queue", "diagnostic:collect_specimen", "diagnostic:publish_result",
        "diagnostic:flag_critical"
    },
    HealthcareRole.PHARMACY_USER: {
        "medication:read_queue", "medication:check_stock", "medication:dispense"
    },
    HealthcareRole.TRANSPORT_OPERATOR: {
        "transport:read_queue", "transport:dispatch", "transport:update_gps", "transport:arrive"
    },
    HealthcareRole.FACILITY_ADMIN: {
        "facility:manage_roster", "facility:update_capacity", "analytics:read_facility"
    },
    HealthcareRole.DISTRICT_MANAGER: {
        "command_centre:read", "analytics:read_district", "referral:monitor_leakage",
        "equity:read_analytics", "audit:read_summary"
    },
    HealthcareRole.STATE_MANAGER: {
        "command_centre:read_state", "analytics:read_state", "equity:read_state"
    },
    HealthcareRole.SYSTEM_ADMIN: {
        "system:manage_config", "integrations:manage", "user:manage"
    },
    HealthcareRole.AUDITOR: {
        "audit:read_all", "compliance:verify_dpdp", "fhir:verify_conformance"
    }
}


class AccessControlEngine:
    """Evaluates RBAC and ABAC access decisions."""

    @staticmethod
    def is_authorized(
        role: HealthcareRole | str,
        action: str,
        user_facility: Optional[str] = None,
        target_facility: Optional[str] = None,
        user_patient_id: Optional[str] = None,
        target_patient_id: Optional[str] = None
    ) -> bool:
        if isinstance(role, str):
            try:
                role = HealthcareRole(role)
            except ValueError:
                return False

        perms = PERMISSIONS_MATRIX.get(role, set())
        if action not in perms:
            return False

        # ABAC Constraints
        if role == HealthcareRole.PATIENT:
            if user_patient_id and target_patient_id and user_patient_id != target_patient_id:
                return False

        if role in {HealthcareRole.CHO, HealthcareRole.LAB_USER, HealthcareRole.PHARMACY_USER}:
            if user_facility and target_facility and user_facility != target_facility:
                return False

        return True
