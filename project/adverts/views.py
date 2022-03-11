from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic

# Create your views here.
def home(request):
    return render(request, "home.html",{})