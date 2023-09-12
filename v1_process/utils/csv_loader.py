from csv import DictReader

from v1_process.models import SocialSecurity, WithholdingTax, Employee
from v1_process.dictionaries.dictionary import *


def load_company_employees_data(company_data: DictReader, employee_data: DictReader) -> list:
    single_company_data = next(company_data)
    employees = []
    for single_employee_data in employee_data:
        social_security = map_to_social_security(single_company_data, single_employee_data)
        withholding_tax = map_to_withholding_tax(single_company_data, single_employee_data)
        employee = Employee(social_security, withholding_tax)
        employees.append(employee)
    return employees


def map_to_social_security(company_data: str, single_employee_data: str) -> SocialSecurity:
    social_security = SocialSecurity(
        wage_income=single_employee_data[WAGE_INCOME],
        unearned_income=single_employee_data[UNEARNED_INCOME],
        paid_vacations=single_employee_data[PAID_VACATIONS],
        voluntary_mandatory_pension=single_employee_data[VOLUNTARY_MANDATORY_PENSION],
        ibc_vacations=single_employee_data[IBC_VACATIONS],
        regime_type=single_employee_data[REGIME_TYPE],
        top_law_1393=company_data[TOP_LAW_1393],
        integral_percentage_salary=company_data[INTEGRAL_PERCENTAGE_SALARY],
        smlv=company_data[SMLV],
        health_contribute=single_employee_data[HEALTH_CONTRIBUTE],
        health_percentage=single_employee_data[HEALTH_PERCENTAGE],
        pension_contribute=single_employee_data[PENSION_CONTRIBUTE],
        pension_percentage=single_employee_data[PENSION_PERCENTAGE],
        worked_days=0,
        salary_limit=0
    )
    return social_security


def map_to_withholding_tax(company_data: str, single_employee_data: str) -> WithholdingTax:
    withholding_tax = WithholdingTax(
        is_foreigner=single_employee_data[IS_FOREIGNER],
        percentage_foreigner=0,
        gross_total_incomes=single_employee_data[GROSS_TOTAL_INCOMES],
        gross_voluntary_withholding=single_employee_data[GROSS_VOLUNTARY_WITHHOLDING],
        food_bonus=single_employee_data[FOOD_BONUS],
        dependent_sum=single_employee_data[DEPENDENT_SUM],
        procedure_type=single_employee_data[PROCEDURE_TYPE],
        argument_procedure_type=single_employee_data[ARGUMENT_PROCEDURE_TYPE],
        payroll_date=company_data[PAYROLL_MONTH],
        initial_date_contract=single_employee_data[INITIAL_DATE_CONTRACT],
        final_date_contract=single_employee_data[FINAL_DATE_CONTRACT],
        housing_relief=single_employee_data[HOUSING_RELIEF],
        health_relief=single_employee_data[HEALTH_RELIEF],
        housing_relief_cap=company_data[HOUSING_RELIEF_CAP],
        health_relief_cap=company_data[HEALTH_RELIEF_CAP],
        uvt_value=company_data[UVT_VALUE],
        non_constitutive_incomes_cap=company_data[NON_CONSTITUTIVE_INCOMES_CAP],
        minimum_month_salary=company_data[SMLV],
        exempt_percentage=company_data[EXEMPT_PERCENTAGE],
        exempt_cap=company_data[EXEMPT_CAP],
        accumulated_exemption=single_employee_data[ACCUMULATED_EXEMPTION],
        exempts_periodicity=company_data[EXEMPTS_PERIODICITY],
        deductible_percentage=company_data[DEDUCTIBLE_PERCENTAGE],
        deductible_cap=company_data[DEDUCTIBLE_CAP],
        accumulated_deductible=single_employee_data[ACCUMULATED_DEDUCTIBLE],
        voluntary_cap_percentage=company_data[VOLUNTARY_CAP_PERCENTAGE],
        voluntary_cap=company_data[VOLUNTARY_CAP],
        dependent=single_employee_data[DEPENDENT],
        dependent_cap=company_data[DEPENDENT_CAP],
        dependent_percentage=company_data[DEPENDENT_PERCENTAGE]
    )
    return withholding_tax
