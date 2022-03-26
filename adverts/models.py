from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=10)
    favorites = models.ManyToManyField('Advert')

    def __str__(self):
        return u'{0}'.format(self.user)


class Advert(models.Model):
    added_at = models.DateTimeField('date published')
    service_type = models.CharField(max_length=45)
    property_type = models.CharField(max_length=45)
    surface = models.PositiveIntegerField()
    room_count = models.PositiveIntegerField()
    bedroom_count = models.PositiveIntegerField()
    is_furnished = models.BooleanField()
    has_balcony = models.BooleanField()
    has_terrace = models.BooleanField()
    has_elevator = models.BooleanField()
    has_parking = models.BooleanField()
    description = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    warranty_deposit = models.PositiveIntegerField()
    energy_use = models.CharField(max_length=45)
    creator = models.ForeignKey(Account, on_delete=models.CASCADE)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    pictures = models.FileField(upload_to='images/', blank = True, null=True)

    def __str__(self):
        return self.property_type


class ApiAdvert(models.Model):
    adress_1 = models.CharField(max_length=255)
    adress_2 = models.CharField(max_length=255)
    bathrooms = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    created_date = models.DateTimeField('date created', default=timezone.now())
    formatted_address = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    last_seen = models.DateTimeField('date last seen', default=timezone.now())
    latitude = models.CharField(max_length=255)
    listed_date = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    property_type = models.CharField(max_length=255)
    raw_address = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.identifier

    @property
    def surface(self):
        return self.bathrooms*10 + self.bedrooms*10 + random.randint(5, 15)

    @property
    def pieces_number(self):
        return self.bathrooms + self.bedrooms + random.randint(1,3)
