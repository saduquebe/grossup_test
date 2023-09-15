"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import SocialSecurity, Employee, WithholdingTax
from v1_process.dictionaries.table import ranges


class GrossUpService:
    _withholding_tax_final = WithholdingTax()
    _social_security_final = SocialSecurity()
    _final_gross_up: float = 0
    def __init__(
        self, social_security_service: SocialSecurityService,
        withholding_tax_service: WithholdingTaxService,):

        self.social_security_service = social_security_service
        self.withholding_tax_service = withholding_tax_service



    def _internal_method(self, attr):
        return attr

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




    def exec(
        self, withholding_tax: WithholdingTax, 
        social_security: SocialSecurity) -> str:

        # Add the gross up to make the calculus
        withholding_tax_final = withholding_tax
        withholding_tax_final.set_gross_total_incomes(
            withholding_tax.get_gross_total_incomes() + _final_gross_up)
        
        while
        
        
    


    def _save_to_database():
        #Logic to connect to Model class and persist data
    def exec(self) -> str:
        for employee in self.employees:
            self._gross_up(employee.social_security, employee.withholding_tax)

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
