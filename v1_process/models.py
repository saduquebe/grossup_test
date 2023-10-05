from django.db import models


# Create your models here.

class WithholdingTax(models.Model):
    is_foreigner = models.BooleanField(blank=False)
    percentage_foreigner = models.DecimalField(max_digits=10, decimal_places=2)
    gross_total_incomes = models.IntegerField()
    gross_voluntary_withholding = models.IntegerField()
    social_security_values = models.JSONField()
    food_bonus = models.IntegerField()
    dependent_sum = models.IntegerField()
    procedure_type = models.CharField(max_length=1)
    argument_procedure_type = models.DecimalField(max_digits=10, decimal_places=2)
    payroll_date = models.DateField()
    initial_date_contract = models.DateField()
    final_date_contract = models.DateField()
    housing_relief = models.IntegerField()
    health_relief = models.IntegerField()
    housing_relief_cap = models.IntegerField()
    health_relief_cap = models.IntegerField()
    uvt_value = models.IntegerField()
    non_constitutive_incomes_cap = models.IntegerField()
    minimum_month_salary = models.IntegerField()
    exempt_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    exempt_cap = models.IntegerField()
    accumulated_exemption = models.IntegerField()
    exempts_periodicity = models.CharField(max_length=1)
    deductible_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    deductible_cap = models.IntegerField()
    accumulated_deductible = models.IntegerField()
    voluntary_cap_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    voluntary_cap = models.IntegerField()
    dependent = models.BooleanField(blank=False)
    dependent_cap = models.IntegerField()
    dependent_percentage = models.DecimalField(max_digits=10, decimal_places=2)


class SocialSecurity(models.Model):
    wage_income = models.IntegerField()
    unearned_income = models.IntegerField()
    paid_vacations = models.IntegerField()
    voluntary_mandatory_pension = models.IntegerField()
    ibc_vacations = models.IntegerField()
    regime_type = models.IntegerField()
    top_law_1393 = models.DecimalField(max_digits=10, decimal_places=2)
    integral_percentage_salary = models.DecimalField(max_digits=10, decimal_places=2)
    smlv = models.IntegerField()
    health_contribute = models.BooleanField()
    health_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    pension_contribute = models.BooleanField()
    pension_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    worked_days = models.IntegerField()
    salary_limit = models.IntegerField()

class Employee:

    def __init__(self, social_security: SocialSecurity,
                 withholding_tax: WithholdingTax, gross_incomes: float, target_salary: float, 
                 document: str, other_discounts: float):
        self.social_security = social_security
        self.withholding_tax = withholding_tax
        self.gross_incomes = gross_incomes
        self.target_salary = target_salary
        self.document = document
        self.other_discounts = other_discounts


class GrossUp:
    def __init__(self, document: str, gross_up: float):
        self.document = document
        self.gross_up = gross_up

class GlobalProcessDescription:
    _events: list

    def __init__(self):
        self._events = []
    
    def add_event(self, event: str, employee: Employee, process: str):
        self._events.append([event, employee, process])
    
    def get_events(self):
        return self._events