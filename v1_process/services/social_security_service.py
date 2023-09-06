"""
Define if these are methods or functions (instance related or not) to define a class
"""

def incomeCalculation(wage_income, unearned_income, paid_vacations):
    total_incomes = wage_income + unearned_income + paid_vacations
    return total_incomes

def baseLaw1393(top_law_1393, unearned_income, paid_vacations, wage_income):
    total_incomes=incomeCalculation(wage_income, unearned_income, paid_vacations)
    cap_40  = total_incomes * top_law_1393
    excess_law_1393 = unearned_income - cap_40
    return cap_40, excess_law_1393

"""
Service to access namespace 
Fill this service with a list of SocialSecurity objects  
"""
class SocialSecurityService:

    def __init__(self, employee_id, company):
        self.employee_id = employee_id
        self.company = company

    def _internal_method(self, attr):
        return attr

    def public_method(self, attr: int) -> int:
        return attr
    
    def _save_to_database():
        #Logic to connect to Model class and persist data
        return