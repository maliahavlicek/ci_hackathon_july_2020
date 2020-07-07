from django import forms
from .models import StatusInput, MOOD_CHOICES


class CreateStatusForm(forms.Form):
    mood = forms.ChoiceField(widget=forms.RadioSelect, choices=MOOD_CHOICES)
    plans = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), max_length=250, initial="Nothing")
    help = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), max_length=250, initial="Nothing")
    user_id = forms.HiddenInput()

    class Meta:
        model = StatusInput
        fields = [
            'mood',
            'plans',
            'help',
            'user_id',
            'update_date',
        ]
