from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=10)
    favorites = models.ManyToManyField(Advert)


class Advert(models.Model):
    added_at = models.DateTimeField('date published')
    service_type = models.CharField(max_length=45)
    property_type = models.CharField(max_length=45)
    surface = models.IntegerField()
    room_count = models.IntegerField()
    bedroom_count = models.IntegerField()
    is_furnished = models.CharField(max_length=1)
    has_balcony = models.CharField(max_length=1)
    has_terrace = models.CharField(max_length=1)
    has_elevator = models.CharField(max_length=1)
    has_parking = models.CharField(max_length=1)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    warranty_deposit = models.IntegerField()
    energy_use = models.CharField(max_length=45)
    creator_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=45)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=45)
    status = models.CharField(max_length=45)

    def __str__(self):
        return self.property_type


class ApiAdvert(models.Model):
    adress_1 = models.CharField(max_length=255)
    adress_2 = models.CharField(max_length=255)
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    city = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    created_date = models.DateTimeField('date created')
    formatted_address = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255)
    last_seen = models.DateTimeField('date last seen')
    latitude = models.CharField(max_length=255)
    listed_date = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    price = models.IntegerField()
    property_type = models.CharField(max_length=255)
    raw_address = models.CharField(max_length=255)
    removed_date = models.DateTimeField('date removed')
    state = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.identifier
