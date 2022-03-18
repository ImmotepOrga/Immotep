from django.shortcuts import  render, redirect
from .forms import NewUserForm, AccountForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Advert
from .forms import CreateAdvertForm


def home(request):
    return render(request, "home.html", {})

@login_required(login_url='/login/')
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
