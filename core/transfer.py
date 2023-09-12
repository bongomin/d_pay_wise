from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account
from django.db.models import Q


@login_required
def search_user_by_account_number(request):
    accounts = Account.objects.filter(account_status="active")
    accounts = Account.objects.all()

    query = request.POST.get('account_number')
    if query:
        accounts = accounts.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()

    context = {
        "accounts": accounts,
        "query": query
    }
    return render(request, "transfer/searchUserByAccountNumber.html", context)
