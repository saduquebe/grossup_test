"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService


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
        return