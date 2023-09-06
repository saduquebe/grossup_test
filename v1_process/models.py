from django.db import models

# Create your models here.

class WithholdingTax(models.Model):
    is_foreigner = models.BooleanField(blank=False)
    name = models.CharField('name', max_length=128)


class SocialSecurity(models.Model):
    employee_id = models.IntegerField()
    company = models.IntegerField()