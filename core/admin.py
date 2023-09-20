from django.contrib import admin
from core.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'transaction_type', 'receiver', 'sender']
    list_editable = ['amount', 'status', 'transaction_type', 'receiver', 'sender']

admin.site.register(Transaction, TransactionAdmin)