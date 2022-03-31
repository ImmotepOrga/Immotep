from asyncio import format_helpers
from django import forms
from django.forms import ModelForm
from django.views.generic import CreateView
from .models import Advert
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from adverts.models import Account
from django.utils.translation import gettext_lazy as _


class CreateAdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = (
            'service_type', 'property_type', 'surface', 'room_count', 'bedroom_count', 'is_furnished', 'has_balcony',
            'has_terrace', 'has_elevator', 'has_parking', 'description', 'price', 'warranty_deposit', 'energy_use', 'greenhouse_gas', 
            'street_number', 'street_name', 'postal_code', 'city', 'status', 'pictures'
        )
        labels = {
            "service_type": lambda: _("Service type"),
            "property_type": lambda: _("Property type"),
            "surface": lambda: _("Surface"),
            "room_count": lambda: _("Number of rooms"),
            "bedroom_count": lambda: _("Number of bedrooms"),
            "is_furnished": lambda: _("Is furnished"),
            "has_balcony": lambda: _("Has a balcony"),
            "has_terrace": lambda: _("Has a terrace"),
            "has_elevator": lambda: _("Has an elevator"),
            "has_parking": lambda: _("Has a parking lot"),
            "description": lambda: _("Description"),
            "price": lambda: _("Price"),
            "warranty_deposit": lambda: _("Deposit of guarantee"),
            "energy_use": lambda: _("Energy consumption"),
            "greenhouse_gas": lambda: _("Greenhouse gas emissions"),
            "street_number": lambda: _("Street number"),
            "street_name": lambda: _("Street name"),
            "postal_code": lambda: _("Zip code"),
            "city": lambda: _("City"),
            "status": lambda: _("Status of the advert"),
            "pictures": lambda: _("Pictures"),
        }
        energy_gas_categories = (('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),('E', 'E'),('F', 'F'),('G', 'G'))
        service_types = (('Location', 'Location'),('Achat', 'Achat'))
        property_types = (('Appartement', 'Appartement'),('Maison', 'Maison'))
        statuses = (('Active', 'Active'),('Inactive', 'Inactive'))
        widgets = {
            'energy_use': forms.Select(choices=energy_gas_categories),
            'greenhouse_gas': forms.Select(choices=energy_gas_categories),
            'service_type': forms.Select(choices=service_types),
            'property_type': forms.Select(choices=property_types),
            'status': forms.Select(choices=statuses),
            'pictures': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': 'true', 'accept':'image/gif, image/jpeg, image/png'}),
        }
        
    
# Formulaire de création de compte d'après le modèle User de Django
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email", "password1", "password2" )
        labels = {
            "username": lambda: _("Username"),
            "email": lambda: _("E-mail address"),
            "password1": lambda: _("Password"),
            "password2": lambda: _("Confirm password")
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)

        if commit:
            user.save()
        return user

# Formulaire qui complète le profil d'après le modèle Account
class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ( "phone_number", "postal_code" )
        labels = {
            "phone_number": lambda: _("Phone number"),
            "postal_code": lambda: _("Zip code")
        }
    
    def save(self, commit=True):
        user = super(AccountForm, self).save(commit=False)

        if commit:
            user.save()
        return user

# Formulaire d'édition de compte sans le mot de passe'
class EditUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email")
        labels = {
            "username": lambda: _("Username"),
            "email": lambda: _("E-mail address")
        }

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)

        if commit:
            user.save()
        return user