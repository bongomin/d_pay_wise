from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import Account
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
from decimal import Decimal


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
        if sender_account.account_balance >= Decimal(amount):
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


def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)

        context = {
            "account":account,
            "transaction":transaction
        }

        return render(request,"transfer/transfer-confirmation.html", context)

    except:
        messages.warning(request,"Transaction does not exist, Try again later ...")
        return redirect("account:account")


def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)

        context = {
            "account":account,
            "transaction":transaction
        }

        return render(request,"transfer/transfer-completed.html", context)

    except:
        messages.warning(request,"Transfer does not exist !")
        return redirect("account:account")

def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    sender = request.user
    receiver = account.user

    sender_account = request.user.account
    receiver_account = account

    completed = False

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        if pin_number == sender_account.account_pin_number:
            transaction.status = "completed"
            transaction.save()

            # deduct money from my account and update my  account balance
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # add amount removed from my account and add it to the account i am sending it to
            account.account_balance += transaction.amount
            account.save()

            messages.success(request, "Transfer Successfull")
            return redirect("core:transfer-completed",account.account_number ,transaction.transaction_id)

        else:
            messages.warning(request, "Pin number not correct")
            return redirect("core:transfer-confirmation", account.account_number ,transaction.transaction_id)

    else:
        messages.warning(request, "Error Occured, Try again Later")
        return redirect("account:account", account.account_number ,transaction.transaction_id)



