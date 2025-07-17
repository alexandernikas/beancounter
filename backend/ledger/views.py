from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .services import create_coffee_transaction, get_employee_with_lowest_balance, update_employee_absences

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDim.objects.all().order_by('employee_id')
    serializer_class = EmployeeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = CoffeeProductDim.objects.all()
    serializer_class = CoffeeProductSerializer


class TransactionSummaryViewSet(viewsets.ModelViewSet):
    queryset = CoffeeTransactionSummary.objects.all().order_by('-transaction_id')
    serializer_class = TransactionSummarySerializer


class TransactionDetailViewSet(viewsets.ModelViewSet):
    queryset = CoffeeTransactionDetail.objects.all()
    serializer_class = TransactionDetailSerializer


class LedgerBalanceViewSet(viewsets.ModelViewSet):
    queryset = CoffeeGeneralLedgerBalances.objects.all()
    serializer_class = LedgerBalanceSerializer

## POST method to create transaction summary and details
class CreateCoffeeTransactionView(APIView):
    def post(self, request):
        try:
            purchaser_id = request.data.get("purchaser_id")
            purchases = request.data.get("purchases", [])

            if not purchaser_id or not purchases:
                return Response({"error": "Missing purchaser_id or purchases"}, status=400)

            summary = create_coffee_transaction(purchaser_id, purchases)
            return Response({"transaction_id": summary.transaction_id}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

## GET method that generates next recommended purchaser
class SuggestBuyerView(APIView):
    def get(self, request):
        from .services import get_employee_with_lowest_balance
        suggested = get_employee_with_lowest_balance()
        return Response({
            "suggested_purchaser_id": suggested.employee_id,
            "name": suggested.employee_name
        })

class UpdateEmployeeAbsencesView(APIView):
    def post(self, request):
        absent_ids = request.data.get('absent_employee_ids', [])

        if not isinstance(absent_ids, list):
            return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        update_employee_absences(absent_ids)
        return Response({'message': 'Employee absences updated.'}, status=status.HTTP_200_OK)

