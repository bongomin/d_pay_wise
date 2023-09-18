from core.models import Transaction
from django.shortcuts import render,redirect
from account.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render

def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user).order_by("-id")
    reciever_transaction = Transaction.objects.filter(receiver=request.user).order_by("-id")

    context = {
        "sender": sender_transaction,
        "receiver": reciever_transaction
    }

    return render(request, "transaction/transaction-list.html", context)
