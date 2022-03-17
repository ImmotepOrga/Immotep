from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Advert
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


def udpate_advert(request, id):
    advert = Advert.objects.get(id=id)

    if request.method == 'POST':
        form = CreateAdvertForm(request.POST, instance=advert)
        if form.is_valid():
            form.save()
            # return HttpResponseRedirect(reverse('detail-advert', advert.id))
            return HttpResponseRedirect(reverse('home'))
    else:
        form = CreateAdvertForm(instance=advert)
    return render(request,'update_advert_form.html',{'update_advert_form': form})