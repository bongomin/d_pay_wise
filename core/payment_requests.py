from core.models import Transaction
from django.shortcuts import render,redirect
from account.models import Account,KYC
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404

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

def AmountRequestProcess(request, account_number):
    try:
        account = get_object_or_404(Account, account_number=account_number)
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
                status="request_processing",
                transaction_type="request"
            )
            new_request.save()

            transaction_id = new_request.transaction_id
            account_number = account.account_number
            return redirect("core:amount-request-process-confirmation", account_number, transaction_id)

        else:
            messages.warning(request, "Error occurred. Please try again later.")
            return redirect("core:dashboard")

    except Account.DoesNotExist:
        messages.error(request, "Invalid account number.")
        return redirect("core:dashboard")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect("core:dashboard")

def AmountRequestConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
        kyc = KYC.objects.get(user=request.user)


        context = {
            "account":account,
            "transaction":transaction,
            "kyc":kyc
        }

        return render(request, "payment_request/amount-request-confirmation.html", context)

    except:
        messages.warning(request,"Transaction does not exist, Try again later ...")
        return redirect("account:account")

def AmountRequestFinalProcess(request, account_number, transaction_id):
    account = get_object_or_404(Account, account_number=account_number)
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.account_pin_number:
            transaction.status = "request_sent"
            transaction.save()

            messages.success(request, "Your payment request has been sent successfully")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Error occurred. Try again later.")
            return redirect("account:dashboard")

def RequestCompleted(request, account_number, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    account = Account.objects.get(account_number=account_number)
    kyc = KYC.objects.get(user=request.user)

    context = {
            "transaction":transaction,
            "kyc":kyc
        }
    messages.success(request, "Request made Successfully")
    return render(request, "payment_request/amount-request-completed.html", context)

