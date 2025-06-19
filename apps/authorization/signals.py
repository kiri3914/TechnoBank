from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from apps.mainapp.models import BankAccount
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(
            user=instance,
            balance=Decimal('100000.00')
        )
        logger.info(f"Счет для пользователя {instance.username} создан.")