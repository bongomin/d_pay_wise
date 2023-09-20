from django.urls import path
from core import views
from core import transfer,payment_requests,transaction,views

app_name = "core"

urlpatterns = [
        path("", views.index, name="index"),

        # transfers
        path("search-account/", transfer.search_user_by_account_number, name = "search-account" ),
        path("amount-transfer/<account_number>/", transfer.AmountTransfer, name = "amount-transfer" ),
        path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name = "amount-transfer-process" ),
        path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name = "transfer-confirmation" ),
        path("transfer-process/<account_number>/<transaction_id>/", transfer.TransferProcess, name = "transfer-process" ),
        path("transfer-completed/<account_number>/<transaction_id>/", transfer.TransferCompleted, name = "transfer-completed" ),

        # transactions
        path('transactions/', transaction.transaction_lists, name='transactions'),
        path('transaction-detail/<transaction_id>/', transaction.transaction_detail, name='transaction-detail'),

        # Request Payments
        path('search-user-account/', payment_requests.SearchUserRequest, name='search-user-account'),

        path('amount-request/<account_number>/', payment_requests.AmountRequest, name='amount-request'),

        path('amount-request-process/<account_number>/', payment_requests.AmountRequestProcess, name='amount-request-process'),

        path('amount-request-process-confirmation/<account_number>/<transaction_id>/', payment_requests.AmountRequestConfirmation, name='amount-request-process-confirmation'),

        path('amount-request-final-process/<account_number>/<transaction_id>/', payment_requests.AmountRequestFinalProcess, name='amount-request-final-process'),

        path('amount-request-completed/<account_number>/<transaction_id>/', payment_requests.RequestCompleted, name='amount-request-completed'),
]