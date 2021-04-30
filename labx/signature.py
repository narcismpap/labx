# LabX
# Simple architecture, design and prototype of a Lab Test Result distribution system via QR Codes
# London, Apr 2021 - https://github.com/narcismpap/labx

from hashlib import blake2b


SIGNATURE_KEY = b"QKLyrjqKFp88VXpV6kpwMSd6"


def blake_sign(payload):
    h = blake2b(key=SIGNATURE_KEY, digest_size=16)
    h.update(payload.encode("utf8"))
    return h.hexdigest()


def add_signature(payload):
    return "%s|%s" % (payload, blake_sign(payload))


def check_signature(payload):
    parts = payload.split("|")
    sign = str(parts[-1])
    del parts[-1]

    return blake_sign("|".join(parts)) == sign
