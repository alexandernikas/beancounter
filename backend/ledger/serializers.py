from rest_framework import serializers
from .models import (
    EmployeeDim,
    CoffeeProductDim,
    CoffeeTransactionSummary,
    CoffeeTransactionDetail,
    CoffeeGeneralLedgerBalances
)

class EmployeeSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = EmployeeDim
        fields = '__all__'


class CoffeeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeProductDim
        fields = '__all__'


class TransactionSummarySerializer(serializers.ModelSerializer):
    purchaser_name = serializers.CharField(source='employee.employee_name', read_only=True)

    class Meta:
        model = CoffeeTransactionSummary
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeTransactionDetail
        fields = '__all__'


class LedgerBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeeGeneralLedgerBalances
        fields = '__all__'
