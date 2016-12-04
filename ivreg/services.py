import os
import uuid
import json
import hashlib
import base64
import requests


def generate_request_id():
    return base64.b32encode(uuid.uuid4().bytes).decode('ascii').rstrip('=')


def generate_candidate_codes(candidates):
    return {x: base64.b32encode(os.urandom(5)).decode('ascii')[:5] for x in candidates}


def generate_ballot_id():
    return base64.b32encode(uuid.uuid4().bytes).decode('ascii')[:10]


def verify_vote(data):
    vote_hash = hashlib.sha256((data['ballot_id'] + data['candidate_id'] + data['vcode']).encode('utf-8')).hexdigest()
    for line in requests.get('http://log.rk.sub.lt/').text.splitlines():
        ballot = json.loads(line.strip())
        if ballot['ballot_id'] == data['ballot_id'] and ballot['vote_hash'] == vote_hash:
            return True
    return False
