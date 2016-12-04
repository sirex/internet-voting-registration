import json

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ivreg.models import Voter
from ivreg.forms import RegistrationForm, ValidationForm
from ivreg.services import generate_candidate_codes, generate_ballot_id, generate_request_id


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
                request_id=generate_request_id(),
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


@csrf_exempt
def validate(request):
    if request.method == "POST":
        form = ValidationForm(request.POST)
        if form.is_valid():
            return render(request, 'validation.html', {
                'back': form.cleaned_data['back'],
                'voter': form.cleaned_data['voter'],
            })
        else:
            return render(request, 'validation.html', {
                'form': form,
            })
    else:
        raise Http404


def ballot(request, request_id):
    ballot = Voter.objects.get(request_id=request_id.upper())
    return render(request, 'ballot.html', {
        'ballot': ballot,
        'candidates': json.loads(ballot.candidates),
    })
