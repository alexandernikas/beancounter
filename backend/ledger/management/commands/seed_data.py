from django.core.management.base import BaseCommand
from ledger.models import (
    EmployeeDim, CoffeeProductDim,
    CoffeeTransactionSummary, CoffeeTransactionDetail,
    CoffeeGeneralLedgerBalances
)
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = "Seed initial data for development"

    def handle(self, *args, **kwargs):
        # Clear old data
        CoffeeTransactionDetail.objects.all().delete()
        CoffeeTransactionSummary.objects.all().delete()
        CoffeeGeneralLedgerBalances.objects.all().delete()
        EmployeeDim.objects.all().delete()
        CoffeeProductDim.objects.all().delete()

        # Add employees
        employees = [
            EmployeeDim.objects.create(employee_name="Alice"),
            EmployeeDim.objects.create(employee_name="Bob"),
            EmployeeDim.objects.create(employee_name="Charlie"),
        ]

        # Add products
        products = [
            CoffeeProductDim.objects.create(product_name="Latte", product_price=Decimal('4.50')),
            CoffeeProductDim.objects.create(product_name="Americano", product_price=Decimal('3.25')),
            CoffeeProductDim.objects.create(product_name="Cold Brew", product_price=Decimal('4.75')),
        ]

        # Set product favorites
        for e in employees:
            e.product = random.choice(products)
            e.save()

        # Ledger balances
        for e in employees:
            CoffeeGeneralLedgerBalances.objects.create(employee=e, balance=Decimal('0.00'))

        # Add a transaction summary and detail
        summary = CoffeeTransactionSummary.objects.create(
            transaction_date=timezone.now().date(),
            employee=employees[0],
            transaction_amount=Decimal('13.00'),
        )

        CoffeeTransactionDetail.objects.create(
            transaction=summary,
            product=products[0],
            product_name=products[0].product_name,
            product_price=products[0].product_price,
            purchaser=employees[0],
            debtor=employees[1],
            transaction_date=summary.transaction_date,
        )

        CoffeeTransactionDetail.objects.create(
            transaction=summary,
            product=products[1],
            product_name=products[1].product_name,
            product_price=products[1].product_price,
            purchaser=employees[0],
            debtor=employees[2],
            transaction_date=summary.transaction_date,
        )

        self.stdout.write(self.style.SUCCESS('✅ Sample data seeded successfully.'))
