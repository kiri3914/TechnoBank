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
        required=False,  # Не делаем обязательным изначально
        label='Номер карты получателя',
        widget=forms.TextInput(attrs={'placeholder': 'Введите номер карты (16 цифр)'})
    )
    receiver_phone_number = forms.CharField(
        max_length=15,
        required=False,  # Не делаем обязательным изначально
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

    def clean(self):
        cleaned_data = super().clean()
        transfer_type = cleaned_data.get('transfer_type')
        receiver_card_number = cleaned_data.get('receiver_card_number')
        receiver_phone_number = cleaned_data.get('receiver_phone_number')

        # Проверяем, заполнено ли требуемое поле в зависимости от transfer_type
        if transfer_type == 'card' and not receiver_card_number:
            raise forms.ValidationError("Пожалуйста, введите номер карты.")
        elif transfer_type == 'phone' and not receiver_phone_number:
            raise forms.ValidationError("Пожалуйста, введите номер телефона.")
        elif transfer_type not in ['card', 'phone']:
            raise forms.ValidationError("Выберите тип перевода.")

        # Дополнительная валидация номера карты
        if receiver_card_number and not (len(receiver_card_number) == 16 and receiver_card_number.isdigit()):
            raise forms.ValidationError("Номер карты должен состоять из 16 цифр.")

        return cleaned_data
