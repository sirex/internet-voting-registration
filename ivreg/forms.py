from django import forms


from ivreg.models import Voter


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['voter_id']


class ValidationForm(forms.Form):
    ballot_id = forms.CharField(min_length=1, max_length=10)
    back = forms.URLField()

    class Meta:
        model = Voter
        fields = ['ballot_id']

    def clean_ballot_id(self):
        ballot_id = self.cleaned_data.get('ballot_id')
        if ballot_id:
            try:
                self.cleaned_data['voter'] = Voter.objects.get(ballot_id=ballot_id)
            except Voter.DoesNotExist:
                raise forms.ValidationError('Given ballot id does not exist.')
        return ballot_id


class VerifyForm(forms.Form):
    ballot_id = forms.CharField(label='Biuletenio nr.')
    candidate_id = forms.CharField(label='Kandidato kodas')
    vcode = forms.CharField(label='Patikrinimo kodas')
