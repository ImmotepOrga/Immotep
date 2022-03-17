from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('annonce/ajouter', views.create_advert, name="create-advert"),
    path('annonce/<int:id>/editer', views.udpate_advert, name="update-advert"),
]