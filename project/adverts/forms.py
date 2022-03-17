from asyncio import format_helpers
from django import forms
from django.forms import ModelForm
from django.views.generic import CreateView
from .models import Advert
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class CreateAdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = (
            'added_at', 'service_type', 'property_type', 'surface', 'room_count', 'bedroom_count', 'is_furnished', 'has_balcony',
            'has_terrace', 'has_elevator', 'has_parking', 'description', 'price', 'warranty_deposit', 'energy_use', 'creator',
            'street_number', 'street_name', 'postal_code', 'city', 'status'
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
            "creator": "Auteur de l'annonce",
            "street_number": "Numéro de rue",
            "street_name": "Nom de rue",
            "postal_code": "Code postal",
            "city": "Ville",
            "status": "Statut de l'annonce",
        }
        energy_categories = (('A', 'A'),('B', 'B'),('C', 'C'),('D', 'D'),('E', 'E'),('F', 'F'),('G', 'G'))
        service_types = (('Appartemment', 'Appartemment'),('Maison', 'Maison'))
        property_types = (('Location', 'Location'),('Achat', 'Achat'))
        statuses = (('Active', 'Active'),('Inactive', 'Inactive'))
        widgets = {
            'added_at': forms.DateInput(attrs={'type':'date'}),
            'energy_use': forms.Select(choices=energy_categories),
            'service_type': forms.Select(choices=service_types),
            'property_type': forms.Select(choices=property_types),
            'status': forms.Select(choices=statuses),
        }
    
