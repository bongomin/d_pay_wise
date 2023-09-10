from django.contrib import admin
from account.models import Account,KYC
from userauth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class AccountAdminModel(ImportExportModelAdmin):
    list_editable =['account_status', 'account_balance']
    list_display = ['user', 'account_number', 'account_status', 'account_balance']
    list_filter = ['account_status']


class KYCAdmin(ImportExportModelAdmin):
    model: Account
    search_fields = ['full_name']
    list_display = ['user', 'full_name','mobile','country', 'city']


admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)


