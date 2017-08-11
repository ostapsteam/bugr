import json

from django.core.exceptions import SuspiciousOperation


def get_json(data):
    try:
        return json.loads(data)
    except:
        raise SuspiciousOperation("Can't parse message")
