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
    housing_relief_cap =  models.IntegerField()
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
    employee_id = models.IntegerField()
    company = models.IntegerField()