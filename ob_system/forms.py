from registration.forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from dal import autocomplete

from .models import Archive, Booking, Report, CriminalProfile, CashBail

RANKS = (
    ('OCS', 'OCS'),
    ('OCPD', 'OCPD'),
)


class SignUpForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, required=True, help_text='Required', label='First Name')

    last_name = forms.CharField(max_length=50, required=True, label='Last Name')

    badge_no = forms.IntegerField(required=True, label='Badge No')

    rank = forms.ChoiceField(
        required=True,
        choices=RANKS,
        label='Rank'
    )

    email = forms.EmailField(max_length=250, help_text='Required. Please Input a valid email address', label='Email')

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