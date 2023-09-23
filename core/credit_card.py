from django.shortcuts import render,redirect
from account.models import Account,KYC
from core.models import CreditCard
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Account


def credit_card_details(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    kyc = KYC.objects.get(user=request.user)
    user_account = Account.objects.get(user=request.user)

    context = {
        "account":account,
        "credic_card":credic_card,
        "kyc": kyc
    }
    return render(request, "credit_card/card-detail.html", context)
