from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from decimal import Decimal

from .models import BankAccount, CustomUser, Transfer, Card
from .forms import TransferForm

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


@login_required
def creates(request):
    BankAccount.objects.create(
            user=request.user,
        )
    messages.success(request, 'Создан успешно')
    return redirect('my_accounts')
def delete_bank(request):
    BankAccount.objects.filter(user=request.user).delete()
    messages.success(request, 'Удалено')
    return redirect('my_accounts')
def delete_bank_one(request, pk):
    BankAccount.objects.get(pk=pk).delete()
    messages.success(request, 'Удален')
    return redirect('my_accounts')
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            transfer_type = form.cleaned_data['transfer_type']

            sender_account = BankAccount.objects.filter(user=request.user).first()
            if not sender_account:
                messages.error(request, 'У вас нет счета для перевода.')
                return redirect('transfer_view')
            
            if transfer_type == 'card':
                receiver_card_number = form.cleaned_data['receiver_card_number']
                try: 
                    receiver_card = Card.objects.get(card_number=receiver_card_number)
                    receiver_account = receiver_card.account
                except Card.DoesNotExist:
                    messages.error(request, 'Карта получателя не найдена.')
                    return redirect('transfer_view')
            else:
                receiver_phone = form.cleaned_data['receiver_phone_number']
                try: 
                    receiver_user = CustomUser.objects.get(phone_number=receiver_phone)
                    receiver_account = BankAccount.objects.filter(user=receiver_user).first()
                    if not receiver_account:
                        messages.error(request, f'У пользователя с номером {receiver_phone} нет активных счетов')
                        return redirect('transfer_view')

                except CustomUser.DoesNotExist:
                    messages.error(request, f"Пользователь с номером {receiver_phone} не найден.")
                    return redirect('transfer_view')
            
            if sender_account == receiver_account:
                messages.error(request, 'Нельзя переводить на свой счет.')
                return redirect('transfer_view')

            with transaction.atomic():
                if sender_account.balance >= amount:
                    Transfer.objects.create(
                        sender_account=sender_account,
                        receiver_account=receiver_account,
                        amount=amount,
                        description=description
                    )
                    messages.success(request, f'Перевод на {amount} тенге успешно выполнен!')
                else:
                    messages.error(request, "Недостаточно средств на счете.")
            return redirect('transfer_view')
    else:
        form = TransferForm(initial={'transfer_type': 'card'})
    return render(request, 'transfer.html', {'form': form})

