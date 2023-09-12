from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Import the specific exception
from django.core.exceptions import ObjectDoesNotExist


@login_required
def account_view(request):
    try:
        kyc = KYC.objects.get(user=request.user)
    except ObjectDoesNotExist:  # Catch the specific
        messages.warning(request, "You need to submit your KYC!")
        return redirect("account:kyc-reg")
    account = Account.objects.get(user=request.user)
    context = {
        "account": account,
        "kyc": kyc
    }
    return render(request, "account/account.html", context)


@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)

    except:
        kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(
                request, "KYC form submitted successfully, In review now.")
            return redirect("core:index")
        else:
            print(form.errors)
            print(form.non_field_errors)
    else:
        form = KYCForm(instance=kyc)

    context = {
        "account": account,
        "form": form,
        "kyc": kyc
    }

    return render(request, "account/kyc-form.html", context)
