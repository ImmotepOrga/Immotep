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


class CreateAdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = (
            'added_at', 'service_type', 'property_type', 'surface', 'room_count', 'bedroom_count', 'is_furnished', 'has_balcony',
            'has_terrace', 'has_elevator', 'has_parking', 'description', 'price', 'warranty_deposit', 'energy_use', 'street_number',
            'street_name', 'postal_code', 'city', 'status', 'pictures'
        )
        labels = {
            "added_at": "Ajouté le",
            "service_type": "Type de service",
            "property_type": "Type de bien",
            "surface": "Surface",
            "room_count": "Nombre de pièces",
            "bedroom_count": "Nombre de chambres",
            "is_furnished": "Est meublé",
            "has_balcony": "Possède un balcon",
            "has_terrace": "Possède une terasse",
            "has_elevator": "Possède un ascenseur",
            "has_parking": "Possède un parking",
            "description": "Description",
            "price": "Prix",
            "warranty_deposit": "Dépot de garantie",
            "energy_use": "Consommation énergétique",
            "street_number": "Numéro de rue",
            "street_name": "Nom de rue",
            "postal_code": "Code postal",
            "city": "Ville",
            "status": "Statut de l'annonce",
            "pictures": "Images",
        }
        energy_categories = (('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),('E', 'E'),('F', 'F'),('G', 'G'))
        service_types = (('Location', 'Location'),('Achat', 'Achat'))
        property_types = (('Appartemment', 'Appartemment'),('Maison', 'Maison'))
        statuses = (('Active', 'Active'),('Inactive', 'Inactive'))
        widgets = {
            'added_at': forms.DateInput(attrs={'type':'date'}),
            'energy_use': forms.Select(choices=energy_categories),
            'service_type': forms.Select(choices=service_types),
            'property_type': forms.Select(choices=property_types),
            'status': forms.Select(choices=statuses),
            'pictures': forms.ClearableFileInput(),
        }
        
    
# Formulaire de création de compte d'après le modèle User de Django
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ( "username", "email", "password1", "password2" )
        labels = {
            "username":"Nom d'utilisateur",
            "email":"Adresse e-mail",
            "password1":"Mot de passe",
            "password2":"Confirmer le mot de passe"
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
            "phone_number":"Numéro de téléphone",
            "postal_code":"Code postal"
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
            "username":"Nom d'utilisateur",
            "email":"Adresse e-mail"
        }

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)

        if commit:
            user.save()
        return user