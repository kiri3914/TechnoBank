from django.contrib import admin
from .models import BankAccount, Card, Transfer

# admin.site.register(BankAccount)
# admin.site.register(Card)
# admin.site.register(Transfer)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'balance', 'user')
    readonly_fields = ('account_number',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_holder' ,'card_number', 'expiry_date', 'cvv', 'balance', 'is_active')
    search_fields = ('card_number', 'card_holder')
    readonly_fields = ('card_number', 'expiry_date', 'cvv', 'balance', 'is_active')

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('sender_account', 'receiver_account', 'amount', 'created_at')