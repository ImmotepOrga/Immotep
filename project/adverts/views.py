from django.shortcuts import  render, redirect
from .forms import NewUserForm, AccountForm
from django.contrib.auth import login
from django.contrib import messages

def home(request):
    return render(request, "home.html",{})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        account_form = AccountForm(request.POST)
        if form.is_valid() and account_form.is_valid():
            user = form.save()
            account = account_form.save(commit=False)
            account.user = user
            account.save()
            account_form.save_m2m()

            login(request, user)           
            return redirect("adverts:home")
        else:
            print(form.errors, account_form.errors)
            args = {'form': form, 'account_form': account_form}
            return render(request, 'register.html', args)
    else:
        form = NewUserForm()
        account_form = AccountForm()
    return render (request, "register.html", {"register_form":form, "account_form":account_form})