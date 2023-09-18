from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction


@login_required
def search_user_by_account_number(request):
    # accounts = Account.objects.filter(account_status="active")
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

def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request,"Account does not exists")
        return redirect("core:search-account")
    context = {
        "account": account
    }
    return render(request,"transfer/amount-transfer.html",context)


def AmountTransferProcess(request, account_number):
    sender = request.user ##current logged in user
    account = Account.objects.get(account_number=account_number) ## account for current logged in user
    reciever = account.user ## The person going to receive the money

    sender_account = request.user.account
    receiver_account = account

    if request.method == "POST":
        amount = request.POST.get('amount-send')
        description = request.POST.get('description')
        if sender_account.account_balance > 0 and amount:
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                receiver=reciever,
                receiver_account=receiver_account,
                status="processing",
                transaction_type="transfer"

                )

            new_transaction.save()

            # gettting the new transaction id
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number,transaction_id)
        else:
            messages.warning(request,"Insufficient Funds ...")
            return redirect("core:amount-transfer", account.account_number)

    else:
        messages.warning(request,"error Occured, Try again later ...")
        return redirect("account:account")

