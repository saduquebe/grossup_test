from rest_framework import serializers
from v1_process.models import SocialSecurity, WithholdingTax


class WithholdingTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithholdingTax
        fields = ['is_foreigner', 'name']


class SocialSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialSecurity
        fields = ['employee_id', 'company']