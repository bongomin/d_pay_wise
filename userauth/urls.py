from django.urls import path
from userauth import views

app_name = "userauth"

urlpatterns = [
    path("register/", views.RegisterUserView, name="register-user"),
    path("logout/", views.logoutUserView, name="logout-user")
]