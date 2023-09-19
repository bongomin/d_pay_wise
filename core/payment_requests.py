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
