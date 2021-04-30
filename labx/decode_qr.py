# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

import uuid
from datetime import datetime

from model_result import Result
from signature import check_signature


SUPPORTED_VERSIONS = ["00"]


class QRParseError(Exception):
    pass


def parse_qr(payload):
    if payload is None:
        raise QRParseError("No QR Code provided")

    try:
        s_ver, s_uuid, s_time, s_name, s_outcome, s_sign = payload.split("|")
    except ValueError:
        raise QRParseError("QR code missing data")

    # check signature
    if not check_signature(payload):
        raise QRParseError("Invalid signature")

    r = Result()

    # version
    r.version = s_ver
    if r.version not in SUPPORTED_VERSIONS:
        raise QRParseError("Unsupported QR code revision")

    # test uuid
    try:
        r.test_id = str(uuid.UUID(s_uuid, version=4))
    except ValueError:
        raise QRParseError("Invalid Test ID")

    # timestamp
    try:
        s_time = int(s_time)
        _ = datetime.fromtimestamp(s_time)
        r.timestamp = s_time
    except ValueError:
        raise QRParseError("Invalid timestamp")

    # name
    r.name = s_name.rstrip("0")

    # outcome
    try:
        r.outcome = int(s_outcome[0])
    except ValueError:
        raise QRParseError("Invalid outcome enum")

    if r.outcome not in Result.POSSIBLE_RESULTS:
        raise QRParseError("Invalid test result")

    return r
