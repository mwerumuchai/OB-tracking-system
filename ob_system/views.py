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
@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
def index(request):

    suspect_list = CriminalProfile.objects.all()

    suspect_filter = SearchFilter(request.GET, queryset=suspect_list)

    # return render(request, 'search/searchlist.html', {'filter': suspect_filter})


    return render(request, 'index.html',{'filter': suspect_filter})


# occurrence book
@login_required(login_url='/accounts/login/')
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

                reportingform = ReportingForm(request.POST)
                suspectform = CriminalProfileForm(request.POST)

                if reportingform.is_valid():

                    reporting = reportingform.save(commit=False)
                    reporting.user = request.user
                    reporting.save()

                    return redirect(occurrence_book)

                else:

                    reportingform = ReportingForm()

                if suspectform.is_valid():

                    profile = suspectform.save(commit=False)
                    profile.user = request.user
                    profile.save()

                    return redirect('search')

                else:

                    suspectform = CriminalProfileForm()

                    return render(request, 'occurrence-book/occurrence.html', {'reportingform': reportingform, 'date': date,
                                                                               'bookings': bookings, 'reports': reports,
                                                                               'suspectform': suspectform})

            else:

                reportingform = ReportingForm()
                suspectform = CriminalProfileForm()

                return render(request, 'occurrence-book/occurrence.html', {'reportingform': reportingform, 'date': date,
                                                                           'bookings': bookings, 'reports': reports,
                                                                           'suspectform': suspectform})

        except Exception as exception:

            raise exception

    except Exception as exception:

        raise exception


# Archives page
@login_required(login_url='/accounts/login/')
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
@login_required(login_url='/accounts/login/')
def cash_bail(request):

    '''
    :param request: list of current day bailed out suspects
    :return:
    '''
    date = dt.date.today()

    # now = datetime.datetime.now().strftime('%H:%M:%S')
    bail = CashBail.objects.all()

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

                return render(request, 'occurrence-book/cashbail.html', {'form': form,'date':date,'bail':bail})

        else:

            form = CashBailForm()

            return render(request, 'occurrence-book/cashbail.html', {'form': form,'date':date,'bail':bail})

    except Exception as exception:

        raise exception


# return render(request, 'occurrence-book/cashbail.html',{'date':date,'bail':bail})

@login_required(login_url='/accounts/login/')
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

                return render(request, 'occurrence-book/occurrence.html', {'form': form})

        else:

            form = CriminalProfileForm()

            return render(request, 'occurrence-book/occurrence.html', {'form': form})

    except Exception as exception:

        raise exception

@login_required(login_url='/accounts/login/')
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

@login_required(login_url='/accounts/login/')
def criminal_profile(request, criminalprofile_id_no):

    '''

    :param request: single suspect
    :param criminalprofile_id_no:
    :return: suspect profile and related items
    '''

    try:

        profile = CriminalProfile.objects.get(id_no=criminalprofile_id_no)

        bookings = Booking.objects.filter(criminal=profile).all().order_by('-id')

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
        
@login_required(login_url='/accounts/login/')
def search_results(request):

    try:

        if 'q' in request.GET and request.GET['q']:

            search_term = request.GET.get('q')

            bookings = Booking.search_by_pub_date(search_term).all()

            reportings = Report.search_by_pub_date(search_term).all()

            return render(request, 'archives/archive.html', {'bookings': bookings, 'reportings': reportings})

        else:

            message = "You haven't searched for any term"

            return render(request, 'searched-tag.html', {"message": message,})

    except Exception as exception:
        raise exception

@login_required(login_url='/accounts/login/')
def search(request):

    '''

    :param request: function to search db for searched item
    :return: return related searched items from the database
    '''

    suspect_list = CriminalProfile.objects.all()

    suspect_filter = SearchFilter(request.GET, queryset=suspect_list)

    return render(request, 'search/searchlist.html', {'filter': suspect_filter})
