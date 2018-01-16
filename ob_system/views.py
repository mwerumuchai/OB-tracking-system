from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ob_system.forms import SignUpForm, LoginForm

from django.http import Http404

from .models import Booking, Report, OccurrenceBook

import datetime as dt

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'emailing/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'emailing/account_activation_invalid.html')


# The landing page

def index(request):

    return render(request, 'index.html')


# occurrence book
def occurrence_book(request):

    date = dt.date.today()

    bookings = Booking.current_day_bookings().order_by('-time')

    reports = Report.current_day_reports().order_by('-time')

    return render(request, 'occurrence-book/occurrence.html', {'date': date, 'bookings': bookings, 'reports': reports})


# Archives page
def archives(request):

    try:

        archive = Booking.objects.filter().all().order_by('-id')
    
        return render(request, 'archives/archives.html', {'archive': archive})

    except ValueError:

        raise Http404()


#  Cash bail page
def cash_bail(request):
    return render(request, 'occurrence-book/cashbail.html')

