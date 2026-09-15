import json
from pathlib import Path

def test_contract_files_exist():
    files=list(Path("contracts").glob("*.json"))
    assert len(files) >= 5

def test_idempotent_event_shape():
    p=json.loads(Path("contracts/event_envelope.json").read_text())
    assert p["event_id"]
    assert p["source_system"]
    assert p["event_type"]
    assert p["journey_id"]
