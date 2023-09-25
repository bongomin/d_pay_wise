from django.shortcuts import render,redirect
from account.models import Account,KYC
from core.models import CreditCard
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import Account
from decimal import Decimal


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


# Add money to my Credit Account
def fund_credit_card(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    kyc = KYC.objects.get(user=request.user)
    user_account = Account.objects.get(user=request.user)

    if request.method == "POST" :
        amount = request.POST.get("funding_amount")
        amount = Decimal(amount)
        if amount < account.account_balance:
            # deduct money form persal account to add or fund to the Credit Card
            account.account_balance -= Decimal(amount)
            account.save()

            #  add the deducted amount from the account and top it to the card
            credic_card.amount += Decimal(amount)
            credic_card.save()

            messages.success(request,"Credit card funding successfull")
            return redirect("core:credit-card-details", credic_card.card_id)

        else:
            messages.error(request, "Insufficient funds. Kindly top up and try again.")
            return redirect("core:credit-card-details", credic_card.card_id)
    else:
        messages.error(request, "Error Occured.")
        return redirect("core:credit-card-details", credic_card.card_id)



def withraw_fund_from_card(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        if credic_card.amount >= Decimal(amount):
            account.account_balance += Decimal(amount)
            account.save()

            credic_card.amount -=Decimal(amount)
            credic_card.save()

            messages.success(request, "Withrawal  successfull")
            return redirect("core:credit-card-details", credic_card.card_id)

        else:
            messages.success(request, "Insufficient funds on the Credit card. Kindly top up and try again.")
            return redirect("core:credit-card-details", credic_card.card_id)





