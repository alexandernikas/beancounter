from .models import (
    CoffeeTransactionSummary,
    CoffeeTransactionDetail,
    CoffeeGeneralLedgerBalances,
    CoffeeProductDim,
    EmployeeDim,
)
from django.utils import timezone
from decimal import Decimal
from django.db import transaction, models

def update_employee_absences(absent_employee_ids):
    print(absent_employee_ids)
    """
    *** accepted format ***
    {
        "absent_employee_ids": [101, 102, 103]
    }
    """
    # clears absences
    EmployeeDim.objects.update(is_absent=False)

    # marks employees ticked as OOO on the front end as absent
    EmployeeDim.objects.filter(employee_id__in=absent_employee_ids).update(is_absent=True)

def get_employee_with_lowest_balance():
    ## returns employee with lowest ledger balance next purchaser recommendation
    return (
        CoffeeGeneralLedgerBalances.objects.select_related('employee')
        .order_by('balance')
        .first()
        .employee
    )

# def check_for_absence(employee_id: int) -> bool:
#     return is_absent

## transaction.atomic decorator to ensure that the multi-step record entry is processed as single unit
@transaction.atomic
def create_coffee_transaction(purchaser_id: int, purchases: list[dict]):
    """
    Creates transaction + associated transaction detail records

    purchases format:
    {
    "purchaser_id": 1,
    "purchases": [
        {
        "debtor_id": 1,
        "product_id": 1
        },
        {
        "debtor_id": 2,
        "product_id": 1
        },
        {
        "debtor_id": 3,
        "product_id": 3
        }
    ]
    }
    """
    ## link transaction to purchasing employee
    purchaser = EmployeeDim.objects.get(employee_id=purchaser_id)
    transaction_date = timezone.now().date()

    # load products keyed by product_id
    product_map = {p.product_id: p for p in CoffeeProductDim.objects.all()}
    total_amount = Decimal('0.00')

    for item in purchases:
        total_amount += product_map[item['product_id']].product_price

    ## populate base fields in transaction summary
    summary = CoffeeTransactionSummary.objects.create(
        employee=purchaser,
        transaction_date=transaction_date,
        transaction_amount=total_amount
    )

    ## populate purchases in transaction detail
    for item in purchases:
        product = product_map[item['product_id']]
        debtor = EmployeeDim.objects.get(employee_id=item['debtor_id'])

        CoffeeTransactionDetail.objects.create(
            transaction=summary,
            product=product,
            product_name=product.product_name,
            product_price=product.product_price,
            purchaser=purchaser,
            debtor=debtor,
            transaction_date=transaction_date
        )

        # updates ledger balances
        ## models.F() allows program to modify a model field directly in query
        CoffeeGeneralLedgerBalances.objects.filter(employee=debtor).update(
            balance=models.F('balance') - product.product_price
        )
        CoffeeGeneralLedgerBalances.objects.filter(employee=purchaser).update(
            balance=models.F('balance') + product.product_price
        )

    return summary