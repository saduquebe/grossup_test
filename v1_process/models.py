from django.db import models

# Create your models here.

class WithholdingTax(models.Model):
    is_foreigner = models.BooleanField(blank=False)
    name = models.CharField('name', max_length=128)


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