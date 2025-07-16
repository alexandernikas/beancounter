from django.db import models

# Create your models here.
from django.db import models

class EmployeeDim(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=100)
    product = models.ForeignKey('CoffeeProductDim', on_delete=models.SET_NULL, null=True, blank=True)
    update_date = models.DateField(auto_now=True)
    is_absent = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_name
    class Meta:
        db_table = 'ledger_employee_dim'


class CoffeeProductDim(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.product_name
    class Meta:
        db_table = 'ledger_product_dim'


class CoffeeTransactionSummary(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    transaction_date = models.DateField()
    employee = models.ForeignKey(EmployeeDim, on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Transaction {self.transaction_id} on {self.transaction_date}'
    class Meta:
        db_table = 'ledger_transaction_summary'

class CoffeeTransactionDetail(models.Model):
    transaction_detail_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(CoffeeTransactionSummary, on_delete=models.CASCADE)
    product = models.ForeignKey(CoffeeProductDim, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    purchaser = models.ForeignKey(EmployeeDim, on_delete=models.CASCADE, related_name='purchases')
    debtor = models.ForeignKey(EmployeeDim, on_delete=models.CASCADE, related_name='debts')
    transaction_date = models.DateField()

    def __str__(self):
        return f'Detail {self.transaction_detail_id} of Transaction {self.transaction.transaction_id}'
    class Meta:
        db_table = 'ledger_transaction_detail'


class CoffeeGeneralLedgerBalances(models.Model):
    employee = models.ForeignKey(EmployeeDim, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=8, decimal_places=2)
    update_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.employee.employee_name}: {self.balance}'
    
    class Meta:
        db_table = 'ledger_general_ledger_balances'