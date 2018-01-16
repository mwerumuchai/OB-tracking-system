from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from dal import autocomplete

from .models import Archive

RANKS = (
    ('OCS', 'OCS'),
    ('OCPD', 'OCPD'),
)


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, required=True, help_text='Required', label='First Name')

    last_name = forms.CharField(max_length=50, required=True, label='Last Name')

    badge_no = forms.IntegerField()

    rank = forms.ChoiceField(
        required=True,
        choices=RANKS,
    )

    email = forms.EmailField(max_length=250, help_text='Required. Please Input a valid email address')

    class Meta:

        model = User

        fields = ('first_name', 'last_name', 'badge_no', 'rank', 'email', 'password1', 'password2',)


class LoginForm(UserCreationForm):

    badge_no = forms.IntegerField()

    class Meta:

        model = User

        fields = ('badge_no', 'password1')


class SearchForm(forms.ModelForm):

    pub_date = forms.ModelChoiceField(
        queryset=Archive.objects.all(),
        widget=autocomplete.ModelSelect2(url='search-results')
    )

    class Meta:

        model = Archive

        fields = ('__all__')