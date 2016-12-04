from ivreg.models import Voter


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
    assert resp.location == 'https://example.com/vote/'


def test_ballot(app):
    Voter.objects.create(
        request_id='SLOCQVAMUNCGNDE6Y5I76HPN3Q',
        ballot_id='2EIWLRVNVN',
        candidates='{}',
    )
    app.get('/ballot/SLOCQVAMUNCGNDE6Y5I76HPN3Q/')
