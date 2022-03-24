from django.urls import path, include
from . import views

app_name = "adverts" 

urlpatterns = [
    path('', views.home, name="home"),
    # # Url to take extern api datas
    # path('api/datas', views.get_api_datas, name="api_datas"),
    # # Delete all ApiAdvert
    # path('api/delete', views.delete_all_props, name="delete_api_datas"),
    path('annonce/ajouter', views.create_advert, name="create-advert"),
    path('annonce/<int:id>/editer', views.udpate_advert, name="update-advert"),
    path('annonce/<int:id>/supprimer', views.delete_advert, name="delete-advert"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path('logout', views.logout_request, name="logout"),
]