from django.shortcuts import render,redirect
from userauth.forms import UserRegisterForm

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from  userauth.models import User


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

def LoginUserView(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # means the email from the model is the same as the entered email/ meanning it exists
            user = User.objects.get(email=email)
            user = authenticate(request,email=email,password=password)

            #  check if there is a user
            if user is not None:
                login(request,user)
                messages.success(request,"You are logged in ...")
                return redirect("core:index")

            else:
                messages.warning(request, "username or password is incorrect")
                return redirect("userauth:login-user")

        except:
            messages.warning(request, "User does not exist in the System.")
            return redirect("userauth:login-user")

    else:
        return render(request, "userauth/login.html")

def logoutUserView(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect("userauth:login-user")