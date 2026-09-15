from collections import defaultdict

STATE = {
    "uhI": {
        "providers": [
            {
                "provider_ref": "TN-DH-DEMO",
                "provider_name": "District Hospital",
                "service": "GENERAL_MEDICINE",
                "specialty": "GENERAL_MEDICINE",
                "city": "Dharmapuri",
                "language": "ta",
                "slot_start": "2026-09-15T16:20:00+05:30",
                "availability": "AVAILABLE"
            },
            {
                "provider_ref": "TN-TH-DEMO",
                "provider_name": "Taluk Hospital",
                "service": "GENERAL_MEDICINE",
                "specialty": "GENERAL_MEDICINE",
                "city": "Dharmapuri",
                "language": "ta",
                "slot_start": "2026-09-15T15:10:00+05:30",
                "availability": "LIMITED"
            }
        ],
        "appointments": {}
    },
    "consultations": {},
    "labs": {},
    "ems": {},
    "events": []
}
