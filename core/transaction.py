from core.models import Transaction
from django.shortcuts import render,redirect
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user).order_by("-id")
    receiver_transaction = Transaction.objects.filter(receiver=request.user).order_by("-id")
    kyc = KYC.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)

    context = {
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        "account": account,
        "kyc": kyc
    }

    return render(request, "transaction/transaction-list.html", context)