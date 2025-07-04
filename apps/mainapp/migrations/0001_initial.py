# Generated by Django 4.2.23 on 2025-06-16 06:22

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(default='8ce7fb1716e64711b7f0', max_length=20, unique=True)),
                ('account_type', models.CharField(choices=[('debit', 'Дебетовый'), ('savings', 'Сберегательный'), ('credit', 'Кредитный')], default='debit', max_length=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_accounts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Банковский аккаунт',
                'verbose_name_plural': 'Банковские аккаунты',
            },
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('completed', 'Завершен'), ('failed', 'Ошибка')], default='pending', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receiver_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_transfers', to='mainapp.bankaccount')),
                ('sender_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_transfers', to='mainapp.bankaccount')),
            ],
            options={
                'verbose_name': 'Перевод',
                'verbose_name_plural': 'Переводы',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(max_length=16, unique=True)),
                ('card_type', models.CharField(choices=[('visa', 'Visa'), ('mastercard', 'MasterCard'), ('mir', 'Мир')], max_length=10)),
                ('expiry_date', models.DateField()),
                ('card_holder', models.CharField(max_length=150)),
                ('cvv', models.CharField(max_length=3)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='mainapp.bankaccount')),
            ],
            options={
                'verbose_name': 'Карта',
                'verbose_name_plural': 'Карты',
            },
        ),
    ]
