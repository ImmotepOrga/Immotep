from django.contrib import admin

# Register your models here.

from .models import Account, Advert, ApiAdvert


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class AdvertAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Catégories du bien', {'fields': ['service_type', 'property_type']}),
        ('Caratéristiques', {'fields': ['surface', 'room_count', 'bedroom_count', 'description', 'price', 'warranty_deposit', 'energy_use', 'greenhouse_gas', 'pictures']}),
        ('Adresse', {'fields': ['street_number', 'street_name', 'postal_code', 'city']}),
        ("Paramêtres de l'annonce", {'fields': ['creator', 'added_at', 'status']}),
    ]
    list_display = ('id', 'service_type', 'property_type', 'status')
    list_filter = ['service_type', 'property_type', 'status']


class ApiAdvertAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Catégories du bien', {'fields': ['property_type']}),
        ('Caratéristiques', {'fields': ['bathrooms', 'bedrooms', 'price', 'identifier', 'latitude', 'longitude']}),
        ('Adresse', {'fields': ['adress_1', 'adress_2', 'city', 'county', 'state', 'zip_code', 'formatted_address', 'raw_address']}),
        ("Paramêtres de l'annonce", {'fields': ['created_date', 'last_seen', 'status']}),
    ]
    list_display = ('id', 'property_type', 'created_date', 'last_seen')
    list_filter = ['property_type']


admin.site.register(Account, AccountAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(ApiAdvert, ApiAdvertAdmin)

admin.site.site_header = "Administration d'Immotep"
admin.site.index_title = 'Gestion des ressources'
admin.site.site_title = 'Immotep Admin'
