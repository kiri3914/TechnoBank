from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/<int:pk>', views.bank_account_detail, name='bank_account_detail'),
    path('my_accounts', views.my_accounts, name='my_accounts'),
    path('transfer/', views.transfer_view, name='transfer_view'),
    path('creates/', views.creates, name='creates'),
    path('delete_bank/', views.delete_bank, name='delete_bank'),
    path('delete_bank_one/<int:pk>', views.delete_bank_one, name='delete_bank_one'),



]


