# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

import time
import uuid
from datetime import datetime
from hashlib import blake2b


SUPPORTED_VERSIONS = ["00"]


class ResultException(Exception):
    pass


class Result:
    VERSION = "00"

    RESULT_PENDING = 0
    RESULT_INCONCLUSIVE = 1
    RESULT_POSITIVE = 2
    RESULT_NEGATIVE = 3

    POSSIBLE_RESULTS = [
        RESULT_PENDING,
        RESULT_INCONCLUSIVE,
        RESULT_POSITIVE,
        RESULT_NEGATIVE,
    ]

    def __init__(self):
        self.version = None
        self.name = None
        self.test_id = None
        self.outcome = None
        self.timestamp = None

    def load_from_db(self, result_uuid):
        # mocked for now
        self.version = self.VERSION
        self.name = "John Snow"
        self.test_id = result_uuid
        self.outcome = self.RESULT_NEGATIVE
        self.timestamp = 1619818359

    def to_qr(self):
        return "|".join([
            self.VERSION, 
            str(self.test_id), 
            str(self.timestamp), 
            self.name[:20].ljust(20, "0"), 
            str(self.outcome)
        ])

    def to_dict(self):
        return {
            "version": self.version,
            "name": self.name,
            "test": self.test_id,
            "time": datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%I:%s"),
            "outcome": self.outcome,
        }
