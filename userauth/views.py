from django.shortcuts import render,redirect
from userauth.forms import UserRegisterForm

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages


def RegisterUserView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"hey {username}your account is successfully created!.")
            # username = request.POST.get('email')
            # username = form.cleaned_data.get('email')
            new_user = authenticate(
                username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("core:index")
    if request.user.is_authenticated:
        messages.warning(
                request, f"you are already logged in...")
        return redirect("core:index")

    else:
        form = UserRegisterForm()
    context = {
        "SignUpForm": form
    }
    return render(request, "userauth/register.html", context)


def logoutUserView(request):
    logout(request.user)
    messages.success("You have been logged out.")
    return redirect("userauth.login")