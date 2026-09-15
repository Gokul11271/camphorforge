from dataclasses import dataclass
from typing import Any

@dataclass
class AdapterResult:
    status: str
    data: dict[str, Any]

class MockAdapter:
    system_name = "MOCK"

    def __init__(self, base_url: str = "http://127.0.0.1:9000"):
        self.base_url = base_url

class AbdmAdapter(MockAdapter):
    system_name = "ABDM"

class UhiAdapter(MockAdapter):
    system_name = "UHI"

class EsanjeevaniAdapter(MockAdapter):
    system_name = "eSanjeevani"

class NcdAdapter(MockAdapter):
    system_name = "NP-NCD"

class StateHisLisLmisAdapter(MockAdapter):
    system_name = "STATE"

class EmsAdapter(MockAdapter):
    system_name = "EMS"
