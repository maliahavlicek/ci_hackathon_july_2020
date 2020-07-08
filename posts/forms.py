from django import forms
from .models import Post


class CreatPostForm(forms.Form):
    """
    Form to Create A Family
    """
    status = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    """hero_image = forms.ImageField(label="Hero Image")"""

    class Meta:
        model = Post,
        fields = ["status"]
