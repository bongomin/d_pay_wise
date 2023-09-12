from django.urls import path
from account import views

app_name = "account"

urlpatterns = [
    path("", views.account_view, name="account"),
    path("kyc-reg/", views.kyc_registration, name="kyc-reg"),
]