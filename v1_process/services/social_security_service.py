"""
Define if these are methods or functions (instance related or not) to define a class
"""

def get_income_calculation(wage_income, unearned_income, paid_vacations):
    total_incomes = wage_income + unearned_income + paid_vacations
    return total_incomes

def get_base_law_1393(top_law_1393, unearned_income, paid_vacations, wage_income):
    total_incomes=get_income_calculation(wage_income, unearned_income, paid_vacations)
    cap_40  = total_incomes * top_law_1393
    if (unearned_income - cap_40) < 0:
       excess_law_1393 = 0
    else:
      excess_law_1393 = unearned_income - cap_40
    return cap_40, excess_law_1393

def ibc(wage_income, top_law_1393, unearned_income, paid_vacations,
        ibc_vacations, integral_percentage_salary, smlv, regime_type,
        worked_days, salary_limit):
  cap_40, excess_law_1393=get_base_law_1393(top_law_1393, unearned_income,
                                      paid_vacations, wage_income)
  if regime_type ==1:
    base  = (wage_income * integral_percentage_salary) + ibc_vacations + excess_law_1393
  else:
    base  = wage_income + ibc_vacations + excess_law_1393

  if base < smlv:
    bounded_base_sup  = smlv
  elif base > salary_limit * smlv:
    bounded_base_sup  = salary_limit * smlv
  else:
    bounded_base_sup  = base

  if (bounded_base_sup/30) * wage_income < smlv:
    bounded_base_inf = (smlv/30) * worked_days
  else:
    bounded_base_inf = bounded_base_sup
  return (base, bounded_base_sup, bounded_base_inf)

def get_solidarity_percentage_table(bounded_base, smlv, ranges):
    for start, end, percentage in ranges:
        if bounded_base >= smlv * start and bounded_base < smlv * end:
          return percentage

    return 0

def get_contributions(wage_income, top_law_1393, unearned_income, paid_vacations,
                  ibc_vacations, integral_percentage_salary, smlv, regime_type,
                  health_contribute, health_percentage, pension_contribute,
                  pension_percentage, voluntary_mandatory_pension, worked_days,
                  salary_limit, ranges):
  base, bounded_base_sup, bounded_base_inf = ibc(wage_income, top_law_1393,
                                                 unearned_income,paid_vacations,
                                                 ibc_vacations,
                                                 integral_percentage_salary,
                                                 smlv, regime_type, worked_days,
                                                 salary_limit)
  percentage_solidarity = get_solidarity_percentage_table(bounded_base_sup, smlv,
                                                    ranges)
  if regime_type == 4 or health_contribute == False:
    health  = 0
  else:
    health  = bounded_base_sup * health_percentage

  if regime_type == 4 or pension_contribute == False:
    pension = 0
  else:
    pension = bounded_base_sup * pension_percentage

  fsp = bounded_base_sup * percentage_solidarity

  return(health, pension, fsp, voluntary_mandatory_pension)

"""
Service to access namespace 
Fill this service with a list of SocialSecurity objects  
"""
class SocialSecurityService:

    def exec(socialsecurity):
       return get_contributions(socialsecurity.wage_income, socialsecurity.top_law_1393, 
                                socialsecurity.unearned_income, socialsecurity.paid_vacations,
                                socialsecurity.ibc_vacations, socialsecurity.integral_percentage_salary, 
                                socialsecurity.smlv, socialsecurity.regime_type,
                                socialsecurity.health_contribute, socialsecurity.health_percentage, 
                                socialsecurity.pension_contribute, socialsecurity.pension_percentage, 
                                socialsecurity.voluntary_mandatory_pension, socialsecurity.worked_days,
                                socialsecurity.salary_limit, socialsecurity.ranges)
    
    def _save_to_database():
      #Logic to connect to Model class and persist data
      return
       