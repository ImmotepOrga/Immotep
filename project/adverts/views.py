from django.shortcuts import render, redirect
from .forms import EditUserForm, NewUserForm, AccountForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Account, Advert
from .forms import CreateAdvertForm
from django.template.defaulttags import register



# Access position in a loop
@register.filter
def index(sequence, position):
    return sequence[position]


# RENDER THE HOMEPAGE
def home(request):
    last_added_adverts = Advert.objects.all().order_by('-id')[:3]
    user_favs = [None] * 3
    if request.user.is_authenticated:
        for i in range(len(last_added_adverts)):
            if Account.favorites.through.objects.filter(advert_id = last_added_adverts[i].id, account_id = request.user.id):
                user_favs[i] = last_added_adverts[i].id
    return render(request, "home.html", {'last_user_adverts': last_added_adverts, 'user_favs': user_favs})


# CREER ANNONCE
def create_advert(request):
    if not request.user.is_authenticated:
        messages.warning(request, f"Vous devez être connecté pour poster une annonce")
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.method == 'POST':
            form = CreateAdvertForm(request.POST)
            if form.is_valid():
                form.save()
                # return HttpResponseRedirect(reverse('detail-advert', advert.id))
                messages.success(request, f"L'annonce à bien été créée")
                return HttpResponseRedirect(reverse('adverts:home'))
        else:
            form = CreateAdvertForm()
        return render(request, 'create_advert_form.html', {'create_advert_form': form})


# MODIFIER ANNONCE
def udpate_advert(request, id):
    advert = Advert.objects.get(id=id)

    if not request.user.is_authenticated:
        messages.warning(request, f"Vous devez être connecté pour modifier une annonce")
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.user.id != advert.creator_id:
            messages.warning(request, f"Vous ne pouvez pas éditer une annonce ne vous appartenant pas")
            return HttpResponseRedirect(reverse('adverts:home'))
        else:
            if request.method == 'POST':
                form = CreateAdvertForm(request.POST, instance=advert)
                if form.is_valid():
                    form.save()
                    # return HttpResponseRedirect(reverse('detail-advert', advert.id))
                    messages.success(request, f"L'annonce à bien été mise à jour")
                    return HttpResponseRedirect(reverse('adverts:home'))
            else:
                form = CreateAdvertForm(instance=advert)
            return render(request, 'update_advert_form.html', {'update_advert_form': form})


# SUPPRIMER ANNONCE
def delete_advert(request, id):
    advert = Advert.objects.get(id=id)

    if not request.user.is_authenticated:
        messages.warning(request, f"Vous devez être connecté pour supprimer une annonce")
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.user.id != advert.creator_id:
            messages.warning(request, f"Vous ne pouvez pas supprimer une annonce ne vous appartenant pas")
            return HttpResponseRedirect(reverse('adverts:home'))
        else:
            if request.method == 'POST':
                advert.delete()
                messages.success(request, f"L'annonce à bien été supprimée")
                return HttpResponseRedirect(reverse('adverts:home'))
            return render(request, 'delete_advert.html', {'advert': advert})


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
            args = {'register_form': form, 'account_form': account_form}
            return render(request, 'register.html', args)
    else:
        form = NewUserForm()
        account_form = AccountForm()
    return render(request, "register.html", {"register_form": form, "account_form": account_form})


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
                messages.info(
                    request, f"Vous êtes connecté en tant que {username}.")
                return redirect("adverts:home")
            else:
                messages.error(
                    request, "Nom d'utilisateur ou mot de passe invalide.")
        else:
            messages.error(
                request, "Nom d'utilisateur ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})


# LOGOUT
@login_required(login_url="adverts:login")
def logout_request(request):
    logout(request)
    messages.info(request, f"Vous êtes déconnecté.")
    return redirect("adverts:home")


# AJOUTER UNE ANNONCE EN FAVORI
def add_favorite(request, advert_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        advert = Advert.objects.get(id=advert_id)
        logged_user = Account.objects.get(user = request.user.id)
        logged_user.favorites.add(advert)
        messages.success(request, f"Annonce ajoutée en favori")
        return redirect("adverts:home")

      
# SUPPRIMER UNE ANNONCE DES FAVORIS
def remove_favorite(request, advert_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        advert = Advert.objects.get(id=advert_id)
        Account.favorites.through.objects.filter(advert_id = advert.id, account_id = request.user.id).delete()
        messages.warning(request, f"Annonce supprimée des favoris")
        return redirect("adverts:home")


# PROFIL
@login_required(login_url="adverts:login")
def account(request):
    user_account = Account.objects.get(id=request.user.id)
    return render(request, "account.html", {"user_account":user_account})

# MODIFIER PROFIL
def update_account(request):
    current_user=request.user
    current_account = Account.objects.get(user = request.user.id)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=current_user)
        account_form = AccountForm(request.POST, instance=current_account)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            account_form.save_m2m()
            messages.success(request, f"Profil modifié avec succès")
            return redirect("adverts:account")
        else:
            args = {'register_form': form, 'account_form': account_form}
            return render(request, 'update_account.html', args)
    else:
        form = EditUserForm(instance=current_user)
        account_form = AccountForm(instance=current_account)
    return render(request, "update_account.html", {"register_form": form, "account_form": account_form})