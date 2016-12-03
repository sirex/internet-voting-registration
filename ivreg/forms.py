from django import forms


from ivreg.models import Voter


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Voter
        fields = ['voter_id']


class ValidationForm(forms.ModelForm):

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
