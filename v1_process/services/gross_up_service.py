"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import SocialSecurity, Employee, WithholdingTax

class GrossUpService:

    def __init__(self, employees: list):
        self.employees = employees
    def _internal_method(self, attr):
        return attr

    def _gross_up(self, social_security:SocialSecurity,withholding_tax:WithholdingTax):
        pass
    def exec(self) -> str:
        for employee in self.employees:
            self._gross_up(employee.social_security, employee.withholding_tax)
    
    def _save_to_database(self):
        #Logic to connect to Model class and persist data
        return