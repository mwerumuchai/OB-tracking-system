from django.shortcuts import render

# Create your views here.

# The landing page
def index(request):
    return render(request,'index.html')

# occurrence book
def occurrence_book(request):
    return render(request,'occurrence-book/occurrence.html')

# Archives page
def archives(request):
    return render(request,'occurrence-book/archives.html')

#  Cash bail page
def cash_bail(request):
    return render(request,'occurrence-book/cashbail.html')
