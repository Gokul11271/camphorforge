import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from careflow_fhir.version import FHIR_VERSION, ABDM_IG_VERSION
from careflow_fhir.builders import patient_resource, service_request_resource, task_resource, consent_resource
from careflow_fhir.bundle import transaction_bundle

def test_versions_pinned():
    assert FHIR_VERSION == "4.0.1"
    assert ABDM_IG_VERSION == "6.5.0"

def test_patient_has_fhir_type_and_identity():
    r = patient_resource("p1","Synthetic Patient","DEMO-ABHA-1")
    assert r["resourceType"]=="Patient"
    assert r["identifier"][0]["value"]=="DEMO-ABHA-1"

def test_service_request_has_required_shape():
    r = service_request_resource("sr1","p1","DEMO","Specialist review")
    for k in ["resourceType","status","intent","subject"]:
        assert k in r

def test_task_links_patient():
    r = task_resource("t1","p1")
    assert r["for"]["reference"]=="Patient/p1"

def test_consent_links_patient():
    r = consent_resource("c1","p1")
    assert r["patient"]["reference"]=="Patient/p1"

def test_bundle_contains_resources():
    b = transaction_bundle([patient_resource("p1","Synthetic Patient")])
    assert b["resourceType"]=="Bundle"
    assert b["entry"][0]["resource"]["resourceType"]=="Patient"
