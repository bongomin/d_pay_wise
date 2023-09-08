from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("register/", views.RegisterUserView, name="register-user")
]