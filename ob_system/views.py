from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ob_system.forms import SignUpForm, LoginForm

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

from .models import Booking, Report, Archive, CriminalProfile, CashBail
from .forms import BookingForm, ReportingForm, CriminalProfileForm, CashBailForm

import datetime as dt
import datetime

from dal import autocomplete

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
            message = render_to_string('emailing/account_activation_email.html', {
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

    # if not request.user.is_authenticated():
    #
    #     return Archive.objects.none()

    try:
        date = dt.date.today()

        bookings = Booking.current_day_bookings().order_by('-time')

        reports = Report.current_day_reports().order_by('-time')

        return render(request, 'occurrence-book/occurrence.html', {'date': date, 'bookings': bookings, 'reports': reports})

    except Exception as exception:

        raise exception


# Archives page
def archives(request):

    try:

        archive = Booking.objects.filter().all().order_by('-id')

        return render(request, 'archives/archive.html', {'archive': archive})

    except ValueError:

        raise Http404()


#  Cash bail page
def cash_bail(request):
    date = dt.date.today()

    # now = datetime.datetime.now().strftime('%H:%M:%S')
    bail = CashBail.objects.all()

    return render(request, 'occurrence-book/cashbail.html',{'date':date,'bail':bail})

def search_results(request):

    try:

        if 'pub_date' in request.GET and request.GET["pub_date"]:
            search_term = request.GET.get("pub_date")

            searched_dates = Archive.search_by_pub_date(search_term)

            bookings = Booking.objects.filter(pub_date=searched_dates).all().order_by('-pub_date')

            reportings = Report.objects.filter(pub_date=searched_dates).all().order_by('-pub_date')

            return render(request, 'archives/archive.html', {'bookings': bookings, 'reportings': reportings})

    except Exception as exception:

        raise exception


# class SearchAutocomplete(autocomplete.Select2QuerySetView):
#
#     def get_queryset(self):
#
#         if not self.request.user.is_authenticated():
#
#             return Archive.objects.none()
#
#         query = Archive.objects.all()
#
#         if self.q:
#
#             query = query.filter(pub_date=self.q)
#
#         return query


def book(request):

    try:

        if request.method == 'POST':

            form = BookingForm(request.POST)

            if form.is_valid():
                booking = form.save(commit=False)

                booking.user = request.user

                booking.save()

                return redirect(occurrence_book)

            else:

                form = BookingForm()

                return render(request, 'occurrence-book/occurrence.html', {'form': form})

        else:

            form = BookingForm()

            return render(request, 'occurrence-book/occurrence.html', {'form': form})

    except Exception as exception:

        raise exception


def report(request):

    try:

        if request.method == 'POST':

            form = ReportingForm(request.POST)

            if form.is_valid():

                reporting = form.save(commit=False)

                reporting.user = request.user

                reporting.save()

                return redirect(occurrence_book)

            else:

                form = ReportingForm()

                return render(request, 'occurrence-book/occurrence.html', {'form': form})

        else:

            form = ReportingForm()

            return render(request, 'occurrence-book/occurrence.html', {'form': form})

    except Exception as exception:

        raise exception


def create_criminal_profile(request):

    try:

        if request.method == 'POST':

            form = CriminalProfileForm(request.POST)

            if form.is_valid():

                profile = form.save(commit=False)

                profile.user = request.user

                profile.save()

                return redirect(occurrence_book)

            else:

                form = CriminalProfileForm()

                return render(request, 'occurrence-book/occurrence.html', {'form': form})

        else:

            form = CriminalProfileForm()

            return render(request, 'occurrence-book/occurrence.html', {'form': form})

    except Exception as exception:

        raise exception


def cashbailform(request):

    try:

        if request.method == 'POST':

            form = CashBailForm(request.POST)

            if form.is_valid():

                bail = form.save(commit=False)

                bail.user = request.user

                bail.save()

                return redirect(cash_bail)

            else:

                form = CashBailForm()

                return render(request, 'cashbail/cashbail.html', {'form': form})

        else:

            form = CashBailForm()

            return render(request, 'cashbail/cashbail.html', {'form': form})

    except Exception as exception:

        raise exception


def criminal_profile(request, id_no):

    try:

        profile = CriminalProfile.criminal_profile()

        bookings = Booking.single_criminal_bookng().order_by('-id')

        return render(request, 'profiles/criminal-profile.html', {'profile': profile, 'bookings': bookings})

    except Exception as exception:

        raise exception
