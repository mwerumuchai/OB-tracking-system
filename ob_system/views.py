from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')


def occurrence_book(request):
    return render(request,'occurrence-book/occurrence.html')
