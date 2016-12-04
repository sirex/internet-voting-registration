import json

from unittest import mock
from ivreg.models import Voter
from ivreg.services import verify_vote


def test_index(app):
    app.get('/')


def test_registration(app):
    resp = app.get('/registration/')
    resp.form['voter_id'] = '123'
    resp = resp.form.submit()
    resp = resp.follow()
    voter = Voter.objects.get(voter_id='123')
    assert resp.request.path.startswith('/ballot/%s/' % voter.request_id)


def test_registration_same_voter_id(app):
    Voter.objects.create(
        voter_id='123',
        request_id='SLOCQVAMUNCGNDE6Y5I76HPN3Q',
        ballot_id='2EIWLRVNVN',
        candidates='{}',
    )
    resp = app.get('/registration/')
    resp.form['voter_id'] = '123'
    resp = resp.form.submit()
    assert resp.context['form'].errors == {
        'voter_id': ['Voter with this Autorizacijos numeris already exists.'],
    }


def test_registration_callback(mocker, app):
    mocker.patch('ivreg.views.generate_request_id', return_value='SLOCQVAMUNCGNDE6Y5I76HPN3Q')
    resp = app.post_json('/registration/', {'voter_id': '123'})
    assert resp.json == {'redirect': 'http://localhost:80/ballot/SLOCQVAMUNCGNDE6Y5I76HPN3Q/'}
    voter = Voter.objects.get(voter_id='123')
    assert voter.request_id == 'SLOCQVAMUNCGNDE6Y5I76HPN3Q'
    assert len(voter.ballot_id) == 10


def test_validation_error(app):
    resp = app.get('/validate/', status=404)
    resp = app.post('/validate/', {'ballot_id': '123'})
    assert resp.context['form'].errors == {
        'ballot_id': ['Given ballot id does not exist.'],
        'back': ['This field is required.'],
    }


def test_validation(app):
    Voter.objects.create(
        voter_id='123',
        request_id='SLOCQVAMUNCGNDE6Y5I76HPN3Q',
        ballot_id='2EIWLRVNVN',
        candidates='{}',
    )
    resp = app.post('/validate/', {
        'ballot_id': '2EIWLRVNVN',
        'back': 'https://example.com/vote/',
    })
    assert resp.form['ballot_id'].value == '2EIWLRVNVN'
    assert resp.form['verified'].value == 'true'


def test_ballot(app):
    Voter.objects.create(
        request_id='SLOCQVAMUNCGNDE6Y5I76HPN3Q',
        ballot_id='2EIWLRVNVN',
        candidates='{"Darth Vader": "111", "Yoda": "222", "Luke Skywalker": "333"}',
    )
    app.get('/ballot/SLOCQVAMUNCGNDE6Y5I76HPN3Q/')


def test_verify_code(mocker):
    mocker.patch('requests.get', return_value=mock.Mock(text='\n'.join([
        json.dumps({
            'ballot_id': 'FXYJALEVIJ',
            'vote_hash': 'bf1c7f5dfb58a7ecb3ae71cfadc0fe6aa961f11f7602e284cc8a272e31b90bd1',
        })
    ])))

    verify_vote({
        'ballot_id': 'FXYJALEVIJ',
        'candidate_id': 'EHXGQ',
        'vcode': 'ITOE6PBH',
    })
