import json

from django.http import JsonResponse
from django.shortcuts import render, redirect

from ivreg.models import Voter
from ivreg.forms import RegistrationForm, ValidationForm
from ivreg.services import generate_candidate_codes, generate_ballot_id


CANDIDATES = [
    'Candidate 1',
    'Candidate 2',
    'Candidate 3',
]


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
        form = RegistrationForm(data)
        if form.is_valid():
            voter = Voter.objects.create(
                voter_id=form.cleaned_data['voter_id'],
                ballot_id=generate_ballot_id(),
                candidates=json.dumps(generate_candidate_codes(CANDIDATES))
            )
            if request.content_type == 'application/json':
                return JsonResponse({'redirect': request.build_absolute_uri(voter.get_absolute_url())})
            else:
                return redirect(voter)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {
        'form': form,
    })


def validate(request):
    if request.method == "POST":
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            return JsonResponse({'errors': 'Only application/json requests are accepted.'})
        form = ValidationForm(data)
        if form.is_valid():
            voter = form.cleaned_data['voter']
            return redirect('https://example.com/validate/%s/' % voter.voter_id)
        elif request.content_type == 'application/json':
            return JsonResponse({'errors': form.errors})
    else:
        return JsonResponse({'errors': 'Only POST method allowed.'})


def ballot(request, ballot_id):
    ballot = Voter.objects.get(ballot_id=ballot_id.upper())
    return render(request, 'ballot.html', {
        'ballot': ballot,
        'canidates': json.loads(ballot.candidates),
    })
