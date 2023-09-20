from core.models import Transaction
from django.shortcuts import render,redirect
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q


@login_required
def SearchUserRequest(request):
    account = Account.objects.all()
    query = request.POST.get("account_number")
    kyc = KYC.objects.get(user=request.user)
    user_account = Account.objects.get(user=request.user)

    if query:
        account = account.filter(
            Q(account_number=query)
            ).distinct()

    context = {
                "accounts":account,
                "account":user_account,
                "query": query,
                "kyc":kyc
            }

    return render(request, "payment_request/search-users.html", context)


def AmountRequest(request,account_number):
    account = Account.objects.get(account_number=account_number)
    kyc = KYC.objects.get(user=request.user)
    context = {
        "account": account,
        "kyc":kyc
    }

    return render(request, "payment_request/amount-request.html", context)

def AmountRequestProcess(request,account_number):
    account = Account.objects.get(account_number=account_number)
    sender = request.user
    receiver = account.user
    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        new_request = Transaction.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            sender=sender,
            receiver=receiver,
            sender_account=sender_account,
            receiver_account=receiver_account,
            status="requested",
            transaction_type="request"
        )

        new_request.save()
        transaction_id = new_request.transaction_id
        return redirect("core:request-confirmation",account.account_number, transaction_id)

    else:
        messages.warning(request, "Error Occured,Try again later")
        return redirect("core:dashboard")


