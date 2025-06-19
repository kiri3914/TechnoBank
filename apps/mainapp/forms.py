from django import forms
from .models import BankAccount

class TransferForm(forms.Form):
    transfer_type = forms.ChoiceField(
        choices=[('card', 'Номер карты'), ('phone', 'Номер телефона')],
        initial='card',
        widget=forms.RadioSelect
        )
    receiver_card_number = forms.CharField(
        max_length=20,
        required=False,
        label='Номер карты получателя',
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер карты (16 цифр)'})
        )
    receiver_phone_number = forms.CharField(
        max_length=15,
        required=False,
        label='Номер телефона получателя',
        widget=forms.TextInput(attrs={'placeholder': '+7XXXYYYZZZZ'})
        )
    amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=100.00,
        label='Сумма перевода',
        widget=forms.NumberInput(attrs={'placeholder': 'Введите сумму перевода'})
        )
    description = forms.CharField(
        max_length=200, 
        required=False,
        label='Комментарий',
        widget=forms.Textarea(attrs={'placeholder': 'Введите комментарий', 'rows': 4})
    )


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if 'initial' in kwargs and kwargs['initial'].get('transfer_type') == 'card':
            self.fields['receiver_card_number'].required = True
            self.fields['receiver_phone_number'].required = False
        elif 'initial' in kwargs and kwargs['initial'].get('transfer_type') == 'phone':
            self.fields['receiver_card_number'].required = False
            self.fields['receiver_phone_number'].required = True
    
    def clean_receiver_card_number(self):
        card_number = self.cleaned_data.get('receiver_card_number')
        if card_number and not (len(card_number) == 16 and card_number.isdigit()):
            raise forms.ValidationError('Номер карты должен состаять из 16 цифр')
        return card_number