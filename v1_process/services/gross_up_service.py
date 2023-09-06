"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService


class GrossUpService:

    def __init__(self, social_security_service: SocialSecurityService, withholding_tax_service: WithholdingTaxService):
        self.social_security_service = social_security_service
        self.withholding_tax_service = withholding_tax_service

    def _internal_method(self, attr):
        return attr

    def exec(self) -> str:
        return "Llamado exitoso" , {self.social_security_service.employee_id}
    
    def _save_to_database():
        #Logic to connect to Model class and persist data
        return