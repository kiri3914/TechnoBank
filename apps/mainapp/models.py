from django.db import models
from apps.authorization.models import CustomUser
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


# Модель банковского аккаунта
class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('debit', 'Дебетовый'),
        ('savings', 'Сберегательный'),
        ('credit', 'Кредитный'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bank_accounts')
    account_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:20])
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='debit')
    balance = models.DecimalField(
        max_digits=15,  # Максимальная длина цифр
        decimal_places=2, # Разрешено 2 цифры после точки
        default=0.00, 
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Банковский аккаунт'
        verbose_name_plural = 'Банковские аккаунты'

    def __str__(self):
        return f"{self.user.username} - {self.account_number} ({self.get_account_type_display()})"

# Модель банковской карты
class Card(models.Model):
    CARD_TYPES = (
        ('visa', 'Visa'),
        ('mastercard', 'MasterCard'),
        ('mir', 'Мир'),
    )

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    expiry_date = models.DateField()
    card_holder = models.CharField(max_length=150)
    cvv = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return f"...{self.card_number[-4:]} ({self.card_type}) - {self.card_holder}"

# Модель перевода
class Transfer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('completed', 'Завершен'),
        ('failed', 'Ошибка'),
    )

    sender_account = models.ForeignKey(
        BankAccount, 
        on_delete=models.CASCADE, 
        related_name='sent_transfers'
    )
    receiver_account = models.ForeignKey(
        BankAccount, 
        on_delete=models.CASCADE, 
        related_name='received_transfers'
    )
    amount = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

    def __str__(self):
        return f"{self.sender_account} -> {self.receiver_account}: {self.amount} ({self.status})"
