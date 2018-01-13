from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ob_system.forms import SignUpForm

import datetime as dt


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            badge_no = form.cleaned_data.get('badge_no')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(badge_no=badge_no, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def current_days_records(request):

    date = dt.date.today()

    return render(request, 'ob.html', {'date': date})
