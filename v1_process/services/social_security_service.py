"""
Define if these are methods or functions (instance related or not) to define a class
"""
from v1_process.models import SocialSecurity
from v1_process.dictionaries.dictionary import *

# Calculate total income
def get_income_calculation(wage_income, unearned_income, paid_vacations):
    total_incomes = wage_income + unearned_income + paid_vacations
    return total_incomes

# Calculate base according to Law 1393
def get_base_law_1393(top_law_1393, unearned_income, paid_vacations, wage_income):
    total_incomes = get_income_calculation(wage_income, unearned_income, paid_vacations)
    cap_40 = total_incomes * top_law_1393
    if (unearned_income - cap_40) < 0:
        excess_law_1393 = 0
    else:
        excess_law_1393 = unearned_income - cap_40
    return cap_40, excess_law_1393

# Calculate Integral Base of Contribution (IBC)
def get_ibc(wage_income, top_law_1393, unearned_income, paid_vacations,
            ibc_vacations, integral_percentage_salary, smlv, regime_type,
            worked_days, salary_limit):
    cap_40, excess_law_1393 = get_base_law_1393(top_law_1393, unearned_income,
                                                paid_vacations, wage_income)
    if regime_type == 1:
        base = (wage_income * integral_percentage_salary) + ibc_vacations + excess_law_1393
    else:
        base = wage_income + ibc_vacations + excess_law_1393

    if base < smlv:
        bounded_base_sup = smlv
    elif base > salary_limit * smlv:
        bounded_base_sup = salary_limit * smlv
    else:
        bounded_base_sup = base

    if (bounded_base_sup / 30) * wage_income < smlv:
        bounded_base_inf = (smlv / 30) * worked_days
    else:
        bounded_base_inf = bounded_base_sup
    return base, bounded_base_sup, bounded_base_inf

# Get the solidarity percentage from a table of ranges
# Table of ranges is defined in utils
def get_solidarity_percentage_table(bounded_base, smlv, ranges):
    for start, end, percentage in ranges:
        if bounded_base >= smlv * start and bounded_base < smlv * end:
            return percentage

    return 0

# Calculate social contributions
def get_contributions(wage_income, top_law_1393, unearned_income, paid_vacations,
                      ibc_vacations, integral_percentage_salary, smlv, regime_type,
                      health_contribute, health_percentage, pension_contribute,
                      pension_percentage, voluntary_mandatory_pension, worked_days,
                      salary_limit, ranges):
    base, bounded_base_sup, bounded_base_inf = get_ibc(wage_income, top_law_1393,
                                                       unearned_income, paid_vacations,
                                                       ibc_vacations,
                                                       integral_percentage_salary,
                                                       smlv, regime_type, worked_days,
                                                       salary_limit)
    percentage_solidarity = get_solidarity_percentage_table(bounded_base_sup, smlv,
                                                            ranges)
    if regime_type == 4 or health_contribute == False:
        health = 0
    else:
        health = bounded_base_sup * health_percentage

    if regime_type == 4 or pension_contribute == False:
        pension = 0
    else:
        pension = bounded_base_sup * pension_percentage

    fsp = bounded_base_sup * percentage_solidarity

    return health, pension, fsp, voluntary_mandatory_pension


"""
Service to access namespace 
Fill this service with a list of SocialSecurity objects  
"""

# Class to access the social security service
class SocialSecurityService:
    '''

    def __init__(self, wage_income, top_law_1393, unearned_income, paid_vacations, ibc_vacations,
                 integral_percentage_salary, smlv, regime_type, health_contribute, health_percentage,
                 pension_contribute, pension_percentage, voluntary_mandatory_pension, worked_days, salary_limit):
        self.wage_income = wage_income
        self.top_law_1393 = top_law_1393
        self.unearned_income = unearned_income
        self.paid_vacations = paid_vacations
        self.ibc_vacations = ibc_vacations
        self.integral_percentage_salary = integral_percentage_salary
        self.smlv = smlv
        self.regime_type = regime_type
        self.health_contribute = health_contribute
        self.health_percentage = health_percentage
        self.pension_contribute = pension_contribute
        self.pension_percentage = pension_percentage
        self.voluntary_mandatory_pension = voluntary_mandatory_pension
        self.worked_days = worked_days
        self.salary_limit = salary_limit'''

    # Method to execute the service
    def exec(self, social_security: SocialSecurity, ranges):
        health_contribution, retire_contribution, fsp, mandatory_voluntary_pension = get_contributions(
            social_security.wage_income,
            social_security.top_law_1393,
            social_security.unearned_income,
            social_security.paid_vacations,
            social_security.ibc_vacations,
            social_security.integral_percentage_salary,
            social_security.smlv,
            social_security.regime_type,
            social_security.health_contribute,
            social_security.health_percentage,
            social_security.pension_contribute,
            social_security.pension_percentage,
            social_security.voluntary_mandatory_pension,
            social_security.worked_days,
            social_security.salary_limit, ranges)
        social_sec_values = {
            HEALTH_CONTRIBUTION: int(health_contribution),
            RETIRE_CONTRIBUTION: int(retire_contribution),
            SOLIDARITY_CONTRIBUTION: int(fsp),
            VOLUNTARY_MANDATORY_PENSION_CONTRIBUTION: int(mandatory_voluntary_pension)
        }
        # print(socialSecValues)
        return social_sec_values

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
