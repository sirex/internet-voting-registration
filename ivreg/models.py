from django.db import models
from django.urls import reverse


class Voter(models.Model):
    # And id to associate received voter id with redirect from CEC server
    request_id = models.CharField(max_length=36, unique=True)

    # Voter id (uuid4) comes from CEC server, idetifies real user.
    voter_id = models.CharField(max_length=36, verbose_name="Autorizacijos numeris", unique=True)

    # Voter ballot id (uuid4) will be published, should not be associated with voter id.
    ballot_id = models.CharField(max_length=36, unique=True)

    # Voter candidate codes
    candidates = models.TextField()

    def get_absolute_url(self):
        return reverse('ballot', args=[self.request_id])
