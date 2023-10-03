from django.shortcuts import render
from django.http import HttpRequest
# Create your views here.

def get_homepage(request):
    return render(request,'home.html')
