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


# The landing page
def index(request):
    return render(request, 'index.html')


# occurrence book
def occurrence_book(request):

    date = dt.date.today()

    return render(request, 'occurrence-book/occurrence.html', {'date': date})


# Archives page
def archives(request):

    return render(request, 'occurrence-book/archives.html')


#  Cash bail page
def cash_bail(request):
    return render(request, 'occurrence-book/cashbail.html')

