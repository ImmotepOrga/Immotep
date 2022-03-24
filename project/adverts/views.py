from django.shortcuts import  render, redirect
from .forms import NewUserForm, AccountForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Advert, ApiAdvert
from .forms import CreateAdvertForm
import requests
from datetime import date

#HOME
def home(request):
    props = get_other_propertries().order_by('-id')[:3]
    return render(request, "home.html", {'properties': props})

def get_other_propertries():
    res = ApiAdvert.objects.all()
    return res

def get_api_datas(request):
    url = "https://realty-mole-property-api.p.rapidapi.com/saleListings"
    querystring = {"state":"TX"}
    headers = {
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com",
        "X-RapidAPI-Key": "f0a7b7d00dmsh96a7932c1eb5c47p156174jsndeceb283db84"
    }

    api = requests.request("GET", url, headers=headers, params=querystring).json()
    for prop in api:
        property = ApiAdvert()
        property.adress_1 = prop["addressLine1"]
        property.bathrooms = round(prop.get("bathrooms", 0))
        property.bedrooms = round(prop.get("bedrooms", 0))
        property.city = prop["city"]
        property.county = prop["county"]
        property.price = prop["price"]
        property.property_type = prop["propertyType"]
        property.state = prop["state"]
        property.zip_code = prop["zipCode"]
        property.last_seen = prop["lastSeen"]
        property.created_date = prop.get("createdDate", date.today())
        property.save()
    props = ApiAdvert.objects.all()
    return render(request, "home.html", {'properties': props})

def delete_all_props(request):
    props = ApiAdvert.objects.all()
    props.delete()
    return render(request, "home.html", {'properties': props})


def create_advert(request):
    if request.method == 'POST':
        form = CreateAdvertForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adverts:home'))
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
            return HttpResponseRedirect(reverse('adverts:home'))
    else:
        form = CreateAdvertForm(instance=advert)
    return render(request,'update_advert_form.html',{'update_advert_form': form})


def delete_advert(request, id):
    advert = Advert.objects.get(id=id)

    if request.method == 'POST':
        advert.delete()
        return HttpResponseRedirect(reverse('adverts:home'))
    return render(request,'delete_advert.html',{'advert': advert})

  
# REGISTER
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        account_form = AccountForm(request.POST)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            account_form.save_m2m()

            login(request, user)           
            return redirect("adverts:home")
        else:
            print(form.errors, account_form.errors)
            args = {'form': form, 'account_form': account_form}
            return render(request, 'register.html', args)
    else:
        form = NewUserForm()
        account_form = AccountForm()
    return render (request, "register.html", {"register_form":form, "account_form":account_form})

# LOGIN
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Vous êtes connecté en tant que {username}.")
                return redirect("adverts:home")
            else:
                messages.error(request,"Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(request,"Nom d'utilisateur ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, f"Vous êtes déconnecté.")
    return redirect("adverts:home")
