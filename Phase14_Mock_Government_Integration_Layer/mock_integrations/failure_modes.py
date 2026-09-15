from enum import Enum

class FailureMode(str, Enum):
    TIMEOUT = "TIMEOUT"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    DUPLICATE = "DUPLICATE"
    STALE_DATA = "STALE_DATA"
    CALLBACK_DELAY = "CALLBACK_DELAY"
    AUTH_EXPIRED = "AUTH_EXPIRED"

# Integration tests should force these conditions at the adapter boundary.
# The core must treat external success as provisional until an acknowledgement/callback
# is received when the external contract requires one.
