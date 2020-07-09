from django import forms
from .models import Post
from django.template.defaultfilters import filesizeformat


class CreatePostForm(forms.Form):
    """
    Form to Share a Text Post
    """
    status = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Post,
        fields = ["status"]


class CreateImageForm(forms.Form):
    """
    Form to Share a Image Post
    """
    photo = forms.ImageField(label="Share Image")

    class Meta:
        model = Post
        fields = [
            'photo',
        ]

    def clean_hero_image(self):
        image_file = self.cleaned_data.get('photo')
        if image_file:
            # limit images to 10 MB
            size_limit = 10485760
            if image_file.size > size_limit:
                self.add_error('hero_image', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(image_file.size)))
