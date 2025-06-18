from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BankAccount, CustomUser

def index(request):
    bank_accounts = BankAccount.objects.all()
    context = {
        'bank_accounts': bank_accounts
    }
    return render(request, 'index.html', context=context)

def bank_account_detail(request, pk):
    bank_account = BankAccount.objects.get(pk=pk)
    context = {
        'account': bank_account
    }
    return render(request, 'bank_account.html', context=context)

@login_required
def my_accounts(request):
    bank_accounts = BankAccount.objects.filter(user=request.user)
    total_balance = sum(account.balance for account in bank_accounts)
    context = {
        'bank_accounts': bank_accounts,
        'total_balance': total_balance
    }
    return render(request, 'my_accounts.html', context=context)