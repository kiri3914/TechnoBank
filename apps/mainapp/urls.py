from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account/<int:pk>', views.bank_account_detail, name='bank_account_detail'),
    path('my_accounts', views.my_accounts, name='my_accounts'),
    path('transfer/', views.transfer_view, name='transfer_view'),
]


