from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from adverts.models import Account

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
    
