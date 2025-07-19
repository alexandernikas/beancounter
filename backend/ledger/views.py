from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .services import * ## create_coffee_transaction, get_employee_with_lowest_balance, update_employee_absences

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeDim.objects.filter(current_employee=True).order_by('employee_id')
    serializer_class = EmployeeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = CoffeeProductDim.objects.all()
    serializer_class = CoffeeProductSerializer


class TransactionSummaryViewSet(viewsets.ModelViewSet):
    queryset = CoffeeTransactionSummary.objects.all().order_by('-transaction_id')
    serializer_class = TransactionSummarySerializer


class TransactionDetailViewSet(viewsets.ViewSet):
    serializer_class = TransactionDetailSerializer

    def list(self, request, transaction_id=None):
        details = CoffeeTransactionDetail.objects.filter(transaction__transaction_id=transaction_id)
        serializer = self.serializer_class(details, many=True)
        return Response(serializer.data)


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

class SuggestBuyerView(APIView):
    def get(self, request):
        suggested = get_employee_with_lowest_balance()

        if suggested is None:
            return Response(
                {"message": "No eligible employees found."},
                status=status.HTTP_204_NO_CONTENT  # or 404, depending on your use case
            )

        return Response({
            "suggested_purchaser_id": suggested.employee_id,
            "name": suggested.employee_name
        })

## post method to handle OOO
class UpdateEmployeeAbsencesView(APIView):
    def post(self, request):
        absent_ids = request.data.get('absent_employee_ids', [])

        if not isinstance(absent_ids, list):
            return Response({'error': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

        update_employee_absences(absent_ids)
        return Response({'message': 'Employee absences updated.'}, status=status.HTTP_200_OK)

## handles update + create employee records
class SaveBulkEmployeesView(APIView):
    def post(self, request):
        employees = request.data.get('employees', [])
        try:
            result = process_employee_changes(employees)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

## this does not actually delete an employee record, but sets the current_employee field to false
class DeleteEmployeeView(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({"error": "employee_id is required"}, status=400)

        try:
            employee = EmployeeDim.objects.get(employee_id=employee_id)
            employee.current_employee = False
            employee.save()


            return Response({"message": f"Employee {employee_id} marked as inactive."}, status=200)
        except EmployeeDim.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

## delete a transaction + credit balances
class RollbackTransactionView(APIView):
    def post(self, request, transaction_id):
        try:
            result = rollback_transaction(transaction_id)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)