# ledger/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'summaries', TransactionSummaryViewSet)
router.register(r'details', TransactionDetailViewSet, basename='transaction-detail')
router.register(r'balances', LedgerBalanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_transaction/', CreateCoffeeTransactionView.as_view(), name='create_transaction'),
    path('suggest_buyer/', SuggestBuyerView.as_view(), name='suggest_buyer'),
    path('update_absences/', UpdateEmployeeAbsencesView.as_view(), name='update_absences'),
    path('save_bulk_employees/', SaveBulkEmployeesView.as_view(), name='save_bulk_employees'),    
    path('delete_employee/', DeleteEmployeeView.as_view(), name='delete_employee'),
    path('details/<int:transaction_id>/', TransactionDetailViewSet.as_view({'get': 'list'}), name='transaction-detail'),
    path('rollback_transaction/<int:transaction_id>/', RollbackTransactionView.as_view(), name='rollback_transaction'),
]
