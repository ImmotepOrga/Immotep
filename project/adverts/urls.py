from django.urls import path, include
from . import views

app_name = "adverts" 

urlpatterns = [
    path('', views.home, name="home"),
    path('annonce/ajouter', views.create_advert, name="create-advert"),
    path('annonce/<int:id>/editer', views.udpate_advert, name="update-advert"),
    path('annonce/<int:id>/supprimer', views.delete_advert, name="delete-advert"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
]