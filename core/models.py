from django.db import models
from userauth.models import User
from account.models import Account
from shortuuid.django_fields import ShortUUIDField

TRANSACTION_TYPE = (
    ("transfer", "Transfer"),
    ("received", "Received"),  # Fixed typo in "received"
    ("refund", "Refund"),
    ("request", "Payment Request"),
    ("none", "None"),
)

TRANSACTION_STATUS = (
    ("failed", "Failed"),
    ("completed", "Completed"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("requested", "Requested"),
    ("request_sent", "request_sent"),
    ("request_settled", "request settled"),
    ("request_processing", "Request Processing"),
)

class Transaction(models.Model):
    transaction_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="TRN")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=1000, default="payment transaction", null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="received_transactions")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_transactions")

    receiver_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="received_transactions_related")
    sender_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sent_transactions_related")

    status = models.CharField(choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, default="none")

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Remove the default value

    def __str__(self):
        try:
            return f"{self.user}"
        except:
            return "Transaction"
