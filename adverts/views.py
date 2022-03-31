from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.defaulttags import register
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Account, Advert, ApiAdvert
from .forms import EditUserForm, NewUserForm, AccountForm, CreateAdvertForm
from datetime import date, datetime
from django.db.models import Q
import requests
import os


# Access position in a loop
@register.filter
def index(sequence, position):
    return sequence[position]


# RENDER THE HOMEPAGE
def home(request):
    props = get_other_propertries()
    last_added_adverts = Advert.objects.all().order_by('-id')[:4]
    user_favs = [None] * 4
    for i in range(len(last_added_adverts)):
        last_added_adverts[i].pictures = [pic.strip() for pic in last_added_adverts[i].pictures.name.split(',')]
        last_added_adverts[i].picture_count = range(len(last_added_adverts[i].pictures))
        if request.user.is_authenticated:
            if Account.favorites.through.objects.filter(advert_id = last_added_adverts[i].id, account_id = request.user.id):
                user_favs[i] = last_added_adverts[i].id
    return render(request, "home.html", {'last_user_adverts': last_added_adverts, 'user_favs': user_favs, 'properties': props})


# FAVORIES LIST
@login_required(login_url="adverts:login")
def favories(request):
    adverts = Account.objects.get(user=request.user.id).favorites.all()
    for i in range(len(adverts)):
        adverts[i].pictures = [pic.strip() for pic in adverts[i].pictures.name.split(',')]
        adverts[i].picture_count = range(len(adverts[i].pictures))
    return render(request, "favories.html", {'user_favs': adverts})


# USER ADVERTS DETAILS
def details_advert(request, id):
    advert = Advert.objects.get(id=id)
    advert.pictures = [pic.strip() for pic in advert.pictures.name.split(',')]
    advert.picture_count = range(len(advert.pictures))
    return render(request, "details-advert.html", {'advert_infos': advert})


def handle_uploaded_files(pictures_list, inserted_advert_id):
    media_folder = 'media/images/'
    if not os.path.exists(media_folder):
        os.mkdir(media_folder)
    os.mkdir(os.path.join(media_folder, inserted_advert_id))
    advert_folder = os.path.join(media_folder, inserted_advert_id)
    for i in range(len(pictures_list)):
        if (i <= 2):
            file_path = os.path.join(advert_folder, pictures_list[i].name)
            open(file_path, 'wb').write(pictures_list[i].read())


# CREER ANNONCE
def create_advert(request):
    if not request.user.is_authenticated:
        messages.warning(request, _("You must be logged in to post an advert"))
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.method == 'POST':
            form = CreateAdvertForm(request.POST, request.FILES)
            if form.is_valid():
                logged_user = Account.objects.get(user=request.user.id)
                partial_advert = form.save(commit=False)
                partial_advert.creator = logged_user

                partial_advert.added_at = datetime.now()

                pictures_list = []
                filenames = []
                for i, file in enumerate(request.FILES.getlist('pictures')):
                    if (i <= 2):
                        pictures_list.append(file)
                        filenames.append(file.name)

                partial_advert.pictures = ', '.join(filenames)

                partial_advert.save()
                inserted_advert = Advert.objects.latest('id')

                handle_uploaded_files(pictures_list, str(inserted_advert.id))

                messages.success(request, _("The advert has been created successfully"))
                return HttpResponseRedirect(reverse('detail-advert', inserted_advert.id))
                # return HttpResponseRedirect(reverse('adverts:home'))
        else:
            form = CreateAdvertForm()
        return render(request, 'create_advert_form.html', {'create_advert_form': form})


# MODIFIER ANNONCE
def udpate_advert(request, id):
    advert = get_object_or_404(Advert, id=id)

    if not request.user.is_authenticated:
        messages.warning(request, _("You must be logged in to edit an advert"))
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.user.id != advert.creator_id:
            messages.warning(request, _("You cannot edit an advert that does not belong to you"))
            return HttpResponseRedirect(reverse('adverts:home'))
        else:
            if request.method == 'POST':
                form = CreateAdvertForm(request.POST, instance=advert)
                if form.is_valid():
                    form.save()
                    messages.success(request, _("The advert has been updated"))
                    return HttpResponseRedirect(reverse('adverts:details-advert', kwargs={'id': advert.id} ))
            else:
                form = CreateAdvertForm(instance=advert)
            return render(request, 'update_advert_form.html', {'update_advert_form': form})


# SUPPRIMER ANNONCE
def delete_advert(request, id):
    advert = get_object_or_404(Advert, id=id)

    if not request.user.is_authenticated:
        messages.warning(request, _("You must be logged in to delete an advert"))
        return HttpResponseRedirect(reverse('adverts:login'))
    else:
        if request.user.id != advert.creator_id:
            messages.warning(request, _("You cannot delete an advert that does not belong to you"))
            return HttpResponseRedirect(reverse('adverts:home'))
        else:
            if request.method == 'POST':
                advert.delete()
                messages.success(request, _("The advert has been deleted"))
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
                messageText = _("You are logged in as")
                messages.info(request, f"{messageText} {username}.")
                return redirect("adverts:home")
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Invalid username or password."))
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})


# LOGOUT
@login_required(login_url="adverts:login")
def logout_request(request):
    logout(request)
    messages.info(request, _("You are disconnected."))
    return redirect("adverts:home")


# AJOUTER UNE ANNONCE EN FAVORI
@login_required(login_url="adverts:login")
def add_favorite(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    logged_user = Account.objects.get(user=request.user.id)
    logged_user.favorites.add(advert)
    messages.success(request, _("Advert added in favorite"))
    return redirect("adverts:home")


# SUPPRIMER UNE ANNONCE DES FAVORIS
@login_required(login_url="adverts:login")
def remove_favorite(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    Account.favorites.through.objects.filter(advert_id = advert.id, account_id = request.user.id).delete()
    messages.warning(request, _("Advert removed from favourites"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# PROFIL
@login_required(login_url="adverts:login")
def account(request):
    user_account = request.user.account
    user_adverts = Advert.objects.filter(creator=request.user.id)
    for i in range(len(user_adverts)):
        user_adverts[i].pictures = [pic.strip() for pic in user_adverts[i].pictures.name.split(',')]
        user_adverts[i].picture_count = range(len(user_adverts[i].pictures))
    return render(request, "account.html", {"user_account":user_account, "user_adverts":user_adverts})

# MODIFIER PROFIL
def update_account(request):
    current_user=request.user
    current_account = request.user.account
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=current_user)
        account_form = AccountForm(request.POST, instance=current_account)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            account_form.save_m2m()
            messages.success(request, _("Profile successfully modified"))
            return redirect("adverts:account")
        else:
            args = {'register_form': form, 'account_form': account_form}
            return render(request, 'update_account.html', args)
    else:
        form = EditUserForm(instance=current_user)
        account_form = AccountForm(instance=current_account)
    return render(request, "update_account.html", {"register_form": form, "account_form": account_form})
  
  
def get_other_propertries():
    res = ApiAdvert.objects.all().order_by('-id')[:3]
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


# PROPERTIES LIST
def properties(request):
    query_params = request.GET
    _city = query_params.get('city')
    _type_purs = query_params.get('type-purs')
    _type_prop = query_params.get("type-prop")
    _pieces = query_params.get("pieces")
    _chambers = query_params.get("chambers")
    _min_surface = query_params.get("min-surface")
    _max_surface = query_params.get("max-surface")
    _min_price = query_params.get("min-price")
    _max_price = query_params.get("max-price")
    _furniture = query_params.get("furniture")
    _terrace = query_params.get("terrace")
    _balcony = query_params.get("balcony")
    _elevator = query_params.get("elevator")
    _parking = query_params.get("parking")

    adverts = Advert.objects.all()

    if _city:
        adverts = adverts.filter(city=_city)
    if _type_prop:
        adverts = adverts.filter(property_type=_type_prop)
    if _type_purs:
        adverts = adverts.filter(service_type=_type_purs)
    if _pieces:
        adverts = adverts.filter(room_count=_pieces)
    if _chambers:
        adverts = adverts.filter(bedroom_count=_chambers)
    if _min_surface:
        adverts = adverts.filter(surface__gte=_min_surface)
    if _max_surface:
        adverts = adverts.filter(surface__lte=_max_surface)
    if _min_price:
        adverts = adverts.filter(price__gte=_min_price)
    if _max_price:
        adverts = adverts.filter(price__lte=_max_price)
    if _furniture:
        adverts = adverts.filter(is_furnished=True)
    if _terrace:
        adverts = adverts.filter(has_terrace=True)
    if _balcony:
        adverts = adverts.filter(has_balcony=True)
    if _elevator:
        adverts = adverts.filter(has_elevator=True)
    if _parking:
        adverts = adverts.filter(has_parking=True)


    user_favs = [None] * len(adverts)
    for i in range(len(adverts)):
        adverts[i].pictures = [pic.strip() for pic in adverts[i].pictures.name.split(',')]
        adverts[i].picture_count = range(len(adverts[i].pictures))
        if request.user.is_authenticated:
            if Account.favorites.through.objects.filter(advert_id = adverts[i].id, account_id = request.user.id):
                user_favs[i] = adverts[i].id
    return render(request, "properties_list.html", {'adverts': adverts, 'user_favs': user_favs})

# ERROR 404
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)