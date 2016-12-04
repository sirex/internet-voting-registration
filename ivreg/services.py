import os
import uuid
import base64


def generate_request_id():
    return base64.b32encode(uuid.uuid4().bytes).decode('ascii').rstrip('=')


def generate_candidate_codes(candidates):
    return {x: base64.b32encode(os.urandom(5)).decode('ascii')[:5] for x in candidates}


def generate_ballot_id():
    return base64.b32encode(uuid.uuid4().bytes).decode('ascii').rstrip('=')
