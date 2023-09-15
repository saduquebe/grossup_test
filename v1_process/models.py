from django.db import models

# Create your models here.

class WithholdingTax(models.Model):
    _is_foreigner = models.BooleanField(blank=False)
    _percentage_foreigner = models.DecimalField(max_digits=10, decimal_places=2)
    _gross_total_incomes = models.IntegerField()
    _gross_voluntary_withholding = models.IntegerField()
    _social_security_values = models.JSONField()
    _food_bonus = models.IntegerField()
    _dependent_sum = models.IntegerField()
    _procedure_type = models.CharField(max_length=1)
    _argument_procedure_type = models.DecimalField(max_digits=10, decimal_places=2)
    _payroll_date = models.DateField()
    _initial_date_contract = models.DateField()
    _final_date_contract = models.DateField()
    _housing_relief = models.IntegerField()
    _health_relief = models.IntegerField()
    _housing_relief_cap =  models.IntegerField()
    _health_relief_cap = models.IntegerField()
    _uvt_value = models.IntegerField()
    _non_constitutive_incomes_cap = models.IntegerField()
    _minimum_month_salary = models.IntegerField()
    _exempt_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    _exempt_cap = models.IntegerField()
    _accumulated_exemption = models.IntegerField()
    _exempts_periodicity = models.CharField(max_length=1)
    _deductible_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    _deductible_cap = models.IntegerField()
    _accumulated_deductible = models.IntegerField()
    _voluntary_cap_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    _voluntary_cap = models.IntegerField()
    _dependent = models.BooleanField(blank=False)
    _dependent_cap = models.IntegerField()
    _dependent_percentage = models.DecimalField(max_digits=10, decimal_places=2)

    def set_gross_total_incomes(self, new_gross_total_incomes):
        self._gross_total_incomes = new_gross_total_incomes
    
    def get_gross_total_incomes(self):
        return _gross_total_incomes




class SocialSecurity(models.Model):
    employee_id = models.IntegerField()
    company = models.IntegerField()