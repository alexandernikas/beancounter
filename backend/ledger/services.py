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
from .UserAgent import NewUserAgent
from bs4 import BeautifulSoup
import json
from .UserAgent import NewUserAgent
from datetime import date
import re
import requests


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
    lowest_balance_record = (
        CoffeeGeneralLedgerBalances.objects
        .filter(employee__current_employee=True)
        .select_related('employee')
        .order_by('balance')
        .first()
    )

    if lowest_balance_record is not None:
        return lowest_balance_record.employee
    else:
        return None


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
            balance=models.F('balance') - product.product_price,
            update_date=timezone.now().date()
        )

        CoffeeGeneralLedgerBalances.objects.filter(employee=purchaser).update(
            balance=models.F('balance') + product.product_price,
            update_date=timezone.now().date()
        )

    return summary


def process_employee_changes(employee_list):
    created = []
    updated = []

    with transaction.atomic():
        for emp in employee_list:
            emp_id = emp.get('employee_id')
            name = emp.get('employee_name')
            product_id = emp.get('product')

            if not name or not product_id:
                continue  # skip incomplete rows

            if emp_id is None:
                # our new employee
                e = EmployeeDim.objects.create(employee_name=name, product_id=product_id)
                created.append(e.employee_id)

                # creates zero balance for new employee
                CoffeeGeneralLedgerBalances.objects.create(
                    employee=e,
                    balance=0  # or use the appropriate field name like `amount=0`
                )

            else:
                ## update existing employee record
                try:
                    e = EmployeeDim.objects.get(employee_id=emp_id)
                    e.employee_name = name
                    e.product_id = product_id
                    e.save()
                    updated.append(emp_id)
                except EmployeeDim.DoesNotExist:
                    continue

    return {
        "created_ids": created,
        "updated_ids": updated,
        "status": "success"
    }


def rollback_transaction(transaction_id):
    try:
        with transaction.atomic():
            ## retrieves transaction_detail records assoicated with transaction_id
            details = CoffeeTransactionDetail.objects.filter(transaction_id=transaction_id)

            if not details.exists():
                raise ValueError(f"No transaction details found for transaction_id={transaction_id}")

            for detail in details:
                # credit debtor balances

                CoffeeGeneralLedgerBalances.objects.filter(employee=detail.debtor_id).update(
                    balance=models.F('balance') + detail.product_price,
                    update_date=timezone.now().date()
                )
                # debit purchaser balance
                CoffeeGeneralLedgerBalances.objects.filter(employee=detail.purchaser_id).update(
                    balance=models.F('balance') - detail.product_price,
                    update_date=timezone.now().date()
                )

            # delete transaction detail records
            details.delete()

            # delete parent record
            summary = CoffeeTransactionSummary.objects.get(pk=transaction_id)
            summary.delete()

            return {"status": "success", "message": f"Transaction {transaction_id} rolled back."}

    except CoffeeTransactionSummary.DoesNotExist:
        raise ValueError(f"Transaction summary with id={transaction_id} does not exist")
    except Employee.DoesNotExist:
        raise ValueError("One or more involved employees no longer exist")
    except Exception as e:
        raise e

def get_menu_html(menu_url):
        UserAgent = NewUserAgent()
        html_raw = None
        response = UserAgent.connect_url(menu_url)
        if response.status_code == 200:
            html_raw = BeautifulSoup(response.content, 'html.parser')
            html_raw = str(html_raw)
        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

def scrape_vento_menu():
    url = "https://ventocoffee.com/pages/print-menu"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    ## find all parent divs that contain a full item block
    blocks = soup.select("span.item-name")
    menu_items = []
    for name_tag in blocks:
        name = name_tag.contents[0].strip() if name_tag.contents else None

        parent = name_tag.find_parent("div")
        if not parent:
            continue

        # The price/size block is likely a sibling after the name/description div
        sibling = parent.find_next_sibling("div", class_="table-drinks")
        if not sibling:
            continue

        sizes = [s.text.strip() for s in sibling.select("div.table-size span.item-size")]
        prices = [p.text.strip() for p in sibling.select("div.table-price span.item-price")]

        # Match size to price
        size_price_map = list(zip(sizes, prices))


        menu_items.append({
            "name": name,
            "sizes_prices": size_price_map,
        })
    print(menu_items)
    return menu_items


