from core.models import Transaction
from django.shortcuts import render,redirect
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404

@login_required
def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    receiver_transaction = Transaction.objects.filter(receiver=request.user, transaction_type="transfer").order_by("-id")
    request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
    request_receiver_transaction = Transaction.objects.filter(receiver=request.user, transaction_type="request")

    kyc = get_object_or_404(KYC, user=request.user)
    account = get_object_or_404(Account, user=request.user)

    context = {
        "sender_transaction": sender_transaction,
        "receiver_transaction": receiver_transaction,
        "request_sender_transaction": request_sender_transaction,
        "request_receiver_transaction": request_receiver_transaction,
        "account": account,
        "kyc": kyc
    }

    return render(request, "transaction/transaction-list.html", context)

@login_required
def transaction_detail(request,transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    kyc = KYC.objects.get(user=request.user)
    account = Account.objects.get(user=request.user)

    context = {
        "transaction":transaction,
        "account": account,
        "kyc": kyc
    }

    return render(request, "transaction/transaction-details.html", context)