from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from ob_system.forms import SignUpForm, LoginForm

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet

from .models import Booking, Report, Archive, CriminalProfile, CashBail
from .forms import BookingForm, ReportingForm, CriminalProfileForm, CashBailForm
from .filters import SearchFilter

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

def officer_login(request):

    try:

        if request.method == 'POST':

            form = LoginForm(request.POST)

            if form.is_valid():

                user = form.save(commit=False)
                user.is_active = True
                user.save()

                return redirect(index)

            else:

                form = LoginForm()

                return render(request, 'login.html', {'form': form})

        else:

            form = LoginForm()

            return render(request, 'login.html', {'form': form})

    except Exception as exception:

        raise exception


def signup(request):

    try:

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

    except Exception as exception:

        raise exception


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
        return redirect('login')
    else:
        return render(request, 'emailing/account_activation_invalid.html')


# The landing page
def index(request):

    return render(request, 'index.html')


# occurrence book
def occurrence_book(request):

    '''
    :param request: current day reports
    :return: current day bookings and reports
    '''

    # if not request.user.is_authenticated():
    #
    #     return Archive.objects.none()

    try:
        date = dt.date.today()

        bookings = Booking.current_day_bookings().order_by('-time')

        reports = Report.current_day_reports().order_by('-time')

        try:

            if request.method == 'POST':

                report_form = ReportingForm(request.POST)

                suspect_form = CriminalProfileForm(request.POST)

                if report_form.is_valid() and suspect_form.is_valid():

                    report_form = form.save(commit=False)

                    suspect_form = form.save(commit=False)

                    report_form.user = request.user

                    report_form.save()

                    suspect_form.user = request.user

                    suspect_form.save()


                    return redirect(occurrence_book)

                else:

                    report_form = ReportingForm()

                    suspect_form = CriminalProfileForm()

                    return render(request, 'occurrence-book/occurrence.html', {'report_form': report_form, 'suspect_form':suspect_form, 'date': date,
                                                                               'bookings': bookings, 'reports': reports})

            else:

                form = ReportingForm()

                return render(request, 'occurrence-book/occurrence.html', {'form': form, 'date': date,
                                                                           'bookings': bookings, 'reports': reports})


        except Exception as exception:

            raise exception

    except Exception as exception:

        raise exception


# Archives page
def archives(request):

    '''
    :param request:
    :return: list of searched record e.g bookings and reports

    '''


    try:

        return render(request, 'archives/archive.html')

    except ValueError:

        raise Http404()


#  Cash bail page
def cash_bail(request):

    '''
    :param request: list of current day bailed out suspects
    :return:
    '''
    date = dt.date.today()

    # now = datetime.datetime.now().strftime('%H:%M:%S')
    bail = CashBail.objects.all()

    return render(request, 'occurrence-book/cashbail.html',{'date':date,'bail':bail})


def create_criminal_profile(request):

    '''
    :param request: function to create a new suspect profile
    :return: created suspect profile
    '''

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

                return render(request, 'occurrence-book/occurrence.html', {'suspectform': form})

        else:

            form = CriminalProfileForm()

            return render(request, 'occurrence-book/occurrence.html', {'suspectform': form})

    except Exception as exception:

        raise exception


def cashbailform(request):

    '''
    :param request: function to record a bailed out suspect
    :return: list of all bailed out suspects
    '''

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


def criminal_profile(request, criminalprofile_id_no):

    '''

    :param request: single suspect
    :param criminalprofile_id_no:
    :return: suspect profile and related items
    '''

    try:

        profile = CriminalProfile.objects.get(id_no=criminalprofile_id_no)

        bookings = Booking.objects.filter(criminal=criminalprofile_id_no).all().order_by('-id')

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

                    return render(request, 'profiles/criminal-profile.html', {'profile': profile, 'bookings': bookings,
                                                                              'form': form})

            else:

                form = BookingForm()

                return render(request, 'profiles/criminal-profile.html', {'profile': profile, 'bookings': bookings,
                                                                          'form': form})

        except Exception as exception:

            raise exception

    except Exception as exception:

        raise exception


def search(request):

    '''

    :param request: function to search db for searched item
    :return: return related searched items from the database
    '''

    suspect_list = CriminalProfile.objects.all()

    suspect_filter = SearchFilter(request.GET, queryset=suspect_list)

    return render(request, 'search/searchlist.html', {'filter': suspect_filter})
