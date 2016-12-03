from ivreg.models import Voter


def test_index(app):
    app.get('/')


def test_registration(app):
    resp = app.get('/registration/')
    resp.form['voter_id'] = '123'
    resp = resp.form.submit()
    resp = resp.follow()
    assert resp.request.path.startswith('/ballot/')


def test_registration_callback(mocker, app):
    mocker.patch('ivreg.views.generate_ballot_id', return_value='2EIWLRVNVNCXFHQDOLXQGIHHAI')
    resp = app.post_json('/registration/', {'voter_id': '123'})
    assert resp.json == {'redirect': 'http://localhost:80/ballot/2EIWLRVNVNCXFHQDOLXQGIHHAI/'}


def test_validation_error(app):
    resp = app.get('/validate/')
    assert resp.json == {'errors': 'Only POST method allowed.'}

    resp = app.post('/validate/', {'ballot_id': '123'})
    assert resp.json == {'errors': 'Only application/json requests are accepted.'}

    resp = app.post_json('/validate/', {'ballot_id': '123'})
    assert resp.json == {'errors': {'ballot_id': ['Given ballot id does not exist.']}}


def test_validation(app):
    Voter.objects.create(voter_id='123', ballot_id='2EIWLRVNVNCXFHQDOLXQGIHHAI', candidates='{}')
    resp = app.post_json('/validate/', {'ballot_id': '2EIWLRVNVNCXFHQDOLXQGIHHAI'})
    assert resp.location == 'https://example.com/validate/123/'


def test_ballot(app):
    Voter.objects.create(ballot_id='2EIWLRVNVNCXFHQDOLXQGIHHAI', candidates='{}')
    app.get('/ballot/2EIWLRVNVNCXFHQDOLXQGIHHAI/')
