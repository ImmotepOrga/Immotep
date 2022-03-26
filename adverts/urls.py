from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "adverts" 

urlpatterns = [
    path('', views.home, name="home"),  
    path('annonce/<int:id>/detail', views.details_advert, name="details-advert"),
    path('annonce/ajouter', views.create_advert, name="create-advert"),
    path('annonce/<int:id>/editer', views.udpate_advert, name="update-advert"),
    path('annonce/<int:id>/supprimer', views.delete_advert, name="delete-advert"),
    path('annonce/favoris', views.favories, name="favories"),
    path('annonce/favori/<int:advert_id>/ajouter', views.add_favorite, name="add-favorite"),
    path('annonce/favori/<int:advert_id>/supprimer', views.remove_favorite, name="remove-favorite"),
    path('annonces', views.properties, name="properties-list"),
    path('inscription', views.register_request, name="register"),
    path('connexion', views.login_request, name="login"),
    path('deconnexion', views.logout_request, name="logout"),
    path('compte', views.account, name="account"),
    path('compte/editer', views.update_account, name="update-account"),
    path('compte/editer/mot-de-passe', auth_views.PasswordChangeView.as_view(template_name='adverts/change-password.html', success_url = '/'), name="update-password"),
    # # Url to take extern api datas
    # path('api/datas', views.get_api_datas, name="api_datas"),
    # # Delete all ApiAdvert
    # path('api/delete', views.delete_all_props, name="delete_api_datas"),
]