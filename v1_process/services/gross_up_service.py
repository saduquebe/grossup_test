"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import SocialSecurity, Employee, WithholdingTax
from v1_process.dictionaries.table import ranges


class GrossUpService:

    def __init__(self, employees: list):
        self.employees = employees
        self.social_security_service = SocialSecurityService()
        self.withholding_tax_service = WithholdingTaxService()

    def _gross_up(self, social_security: SocialSecurity, withholding_tax: WithholdingTax):
        social_security_values = self.social_security_service.exec(social_security, ranges)
        withholding_tax.social_security_values = social_security_values
        withholding_tax_contribution = self.withholding_tax_service.exec(withholding_tax)

        print("PERSONA---------------------------------------------")
        print(social_security_values)
        print(withholding_tax_contribution)


    def exec(self) -> str:
        for employee in self.employees:
            self._gross_up(employee.social_security, employee.withholding_tax)

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
