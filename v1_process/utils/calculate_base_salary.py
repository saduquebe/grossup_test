from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import Employee
from v1_process.dictionaries.table import ranges

def calculate_base_salary(
        employee: Employee, social_security_service: SocialSecurityService,
        withholding_tax_service: WithholdingTaxService
                    ) -> int:
    
    social_security_values = social_security_service.exec(
            employee.social_security, ranges)
    
    employee.withholding_tax.social_security_values = social_security_values

    withholding_tax_contribution = withholding_tax_service.exec(
        employee.withholding_tax)
    
    base = employee.social_security.wage_income
    
    return (
        base - sum(social_security_values.values()) - withholding_tax_contribution
        )