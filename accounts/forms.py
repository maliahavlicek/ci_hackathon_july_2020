from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from users.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Family
from users.models import UserProfile
from django.template.defaultfilters import filesizeformat


class UserLoginForm(forms.Form):
    """ Form to be used by login """
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}
    ))
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('next')
            ),
            Submit('submit', 'Login')
        )


class UserRegistrationFrom(UserCreationForm):
    """Form used to register a new user"""
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'you@example.com'
    }))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        # Make sure email isn't already in system
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            self.add_error(
                'email', 'That email address is already registered.')
        # NOTE: assigned but never used?
        password1 = self.cleaned_data.get('password1')

    def clean_password2(self):
        # Make sure passwords match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Passwords must match.')

        email = self.cleaned_data.get('email')
        if email in password2:
            raise forms.ValidationError(
                'Your email cannot be part of your password.')

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Register')
        )


class ProfileForm(ModelForm):
    """
    A user edit profile form.
    'user' is excluded to probhit username edditing.
    """
    class Meta:
        model = User
        fields = [
          'first_name',
          'last_name',
          'email',
        ]


class ProfileImageForm(ModelForm):
    """
    A user edit profile form.
    This is the form for the profile picture.
    """
    class Meta:
        model = UserProfile
        fields = [
          'profile_picture',
        ]


class CreateFamilyForm(forms.Form):
    """
    Form to Create A Family
    """
    family_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}))
    hero_image = forms.ImageField(label="Hero Image")
    members = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Family
        fields = [
            'family_name',
            'hero_image',
            'members',
        ]

    def clean_hero_image(self):
        image_file = self.cleaned_data.get('hero_image')
        if image_file:
            # limit images to 10 MB
            size_limit = 10485760
            if image_file.size > size_limit:
                self.add_error(
                    'hero_image',
                    'Please keep file size under %s. Current size %s' %
                    (filesizeformat(size_limit),
                     filesizeformat(image_file.size))
                )
