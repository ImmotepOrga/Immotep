from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic
from .forms import CreateAdvertForm

# Create your views here.


def home(request):
    return render(request, "home.html", {})


def create_advert(request):
    if request.method == 'POST':
        form = CreateAdvertForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = CreateAdvertForm()
    return render(request, 'create_advert_form.html', {'create_advert_form': form})
