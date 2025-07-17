# ledger/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'summaries', TransactionSummaryViewSet)
router.register(r'details', TransactionDetailViewSet)
router.register(r'balances', LedgerBalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_transaction/', CreateCoffeeTransactionView.as_view(), name='create_transaction'),
    path('suggest_buyer/', SuggestBuyerView.as_view(), name='suggest_buyer'),
    path('update_absences/', UpdateEmployeeAbsencesView.as_view(), name='update_absences'),

]
