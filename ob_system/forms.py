from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from dal import autocomplete

from .models import Booking, Report, CriminalProfile, CashBail, UserProfile

from nocaptcha_recaptcha import NoReCaptchaField

RANKS = (
    ('OCS', 'OCS'),
    ('OCPD', 'OCPD'),
)


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, required=True, label='First Name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    last_name = forms.CharField(max_length=50, required=True, label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(max_length=250, required=True, label='Email')

    password1 = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'name': "password1",
                                                                                            'type': "password"}))
    password2 = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'name': "password2",
                                                                                            'type': "password"}))

    class Meta:

        model = User

        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)


class SignUpExtendedForm(forms.ModelForm):

    badge_no = forms.IntegerField(required=True, label='Badge No',
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    rank = forms.ChoiceField(
        required=True,
        choices=RANKS,
        label='Rank'
    )

    class Meta:

        model = UserProfile

        fields = ('badge_no', 'rank')


class LoginForm(UserCreationForm):

    badge_no = forms.IntegerField(required=True, label='Badge No',
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                            'name': "password1",
                                                                                            'type': "password"}))

    class Meta:

        model = User

        fields = ('badge_no', 'password1')


class SearchForm(forms.ModelForm):

    pub_date = forms.ModelChoiceField(
        queryset=Booking.objects.all(),
        widget=autocomplete.ModelSelect2(url='search-results')
    )

    class Meta:

        model = Booking

        fields = ('__all__')


class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking

        fields = ('__all__')


class ReportingForm(forms.ModelForm):

    class Meta:

        model = Report

        fields = ('__all__')


class CriminalProfileForm(forms.ModelForm):

    class Meta:

        model = CriminalProfile

        fields = ('__all__')


class CashBailForm(forms.ModelForm):

    class Meta:

        model = CashBail

        fields = ('__all__')
