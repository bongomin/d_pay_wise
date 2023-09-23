from django.contrib import admin
from core.models import Transaction,CreditCard

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'status', 'transaction_type', 'receiver', 'sender']
    list_editable = ['amount', 'status', 'transaction_type', 'receiver', 'sender']

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'card_status', 'card_type', 'month', 'year', 'cvv']
    list_editable = ['amount', 'card_status', 'card_type', 'month', 'year', 'cvv']

admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)