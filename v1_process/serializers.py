from rest_framework import serializers
from v1_process.models import SocialSecurity, WithholdingTax


class WithholdingTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithholdingTax
        fields = ['is_foreigner',
                'percentage_foreigner', 
                'gross_total_incomes',
                'gross_voluntary_withholding', 
                'social_security_values', 
                'food_bonus',
                'dependent_sum', 
                'procedure_type', 
                'argument_procedure_type',
                'payroll_date', 
                'initial_date_contract', 
                'final_date_contract',
                'housing_relief', 
                'health_relief', 
                'housing_relief_cap',
                'health_relief_cap', 
                'uvt_value', 
                'non_constitutive_incomes_cap',
                'minimum_month_salary', 
                'exempt_percentage', 
                'exempt_cap',
                'accumulated_exemption', 
                'exempts_periodicity',
                'deductible_percentage', 
                'deductible_cap', 
                'accumulated_deductible',
                'voluntary_cap_percentage', 
                'voluntary_cap', 
                'dependent',
                'dependent_cap', 
                'dependent_percentage']


class SocialSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialSecurity
        fields = ['employee_id', 'company']