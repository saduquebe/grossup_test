from csv import DictReader

from v1_process.models import SocialSecurity, WithholdingTax, Employee
from v1_process.dictionaries.dictionary import *
from v1_process.dictionaries.table import uvtTable


def load_company_employees_data(single_company_data: str, employee_data: DictReader, targets_data: dict) -> list:

    employees = []
    for single_employee_data in employee_data:
        social_security = map_to_social_security(single_company_data, single_employee_data)
        withholding_tax = map_to_withholding_tax(single_company_data, single_employee_data)

        target_salary = targets_data[single_employee_data[DOCUMENT]]
        other_discounts = float(single_employee_data[OTHER_DISCOUNTS])

        employee = Employee(social_security, withholding_tax, target_salary,
                            single_employee_data[DOCUMENT], other_discounts)
        employees.append(employee)
    return employees


def map_to_social_security(company_data: str, single_employee_data: str) -> SocialSecurity:
    social_security = SocialSecurity(
        wage_income=float(single_employee_data[WAGE_INCOME]),
        unearned_income=float(single_employee_data[UNEARNED_INCOME]),
        paid_vacations=float(single_employee_data[PAID_VACATIONS]),
        voluntary_mandatory_pension=float(single_employee_data[VOLUNTARY_MANDATORY_PENSION]),
        ibc_vacations=float(single_employee_data[IBC_VACATIONS]),
        regime_type=int(single_employee_data[REGIME_TYPE]),
        top_law_1393=float(company_data[TOP_LAW_1393]),
        integral_percentage_salary=float(company_data[INTEGRAL_PERCENTAGE_SALARY]),
        smlv=float(company_data[SMLV]),
        health_contribute=bool(int(single_employee_data[HEALTH_CONTRIBUTE])),
        health_percentage=float(single_employee_data[HEALTH_PERCENTAGE]),
        pension_contribute=bool(int(single_employee_data[PENSION_CONTRIBUTE])),
        pension_percentage=float(single_employee_data[PENSION_PERCENTAGE]),
        worked_days=0,
        salary_limit=float(company_data[SOCIAL_SECURITY_CAP])
    )
    return social_security


def map_to_withholding_tax(company_data: str, single_employee_data: str) -> WithholdingTax:
    withholding_tax = WithholdingTax(
        is_foreigner=bool(int(single_employee_data[IS_FOREIGNER])),
        percentage_foreigner=float(company_data[PERCENTAGE_FOREIGNER]),
        gross_total_incomes=float(single_employee_data[GROSS_TOTAL_INCOMES]),
        gross_voluntary_withholding=float(single_employee_data[GROSS_VOLUNTARY_WITHHOLDING]),
        food_bonus=float(single_employee_data[FOOD_BONUS]),
        dependent_sum=float(single_employee_data[DEPENDENT_SUM]),
        procedure_type=single_employee_data[PROCEDURE_TYPE],
        argument_procedure_type=uvtTable if single_employee_data[PROCEDURE_TYPE] == "T" else float(
            single_employee_data[ARGUMENT_PROCEDURE_TYPE]),
        payroll_date=company_data[PAYROLL_YEAR] + "-" + company_data[PAYROLL_MONTH],
        initial_date_contract=single_employee_data[INITIAL_DATE_CONTRACT],
        final_date_contract=single_employee_data[FINAL_DATE_CONTRACT],
        housing_relief=float(single_employee_data[HOUSING_RELIEF]),
        health_relief=float(single_employee_data[HEALTH_RELIEF]),
        housing_relief_cap=float(company_data[HOUSING_RELIEF_CAP]),
        health_relief_cap=float(company_data[HEALTH_RELIEF_CAP]),
        uvt_value=float(company_data[UVT_VALUE]),
        non_constitutive_incomes_cap=float(company_data[NON_CONSTITUTIVE_INCOMES_CAP]),
        minimum_month_salary=float(company_data[SMLV]),
        exempt_percentage=float(company_data[EXEMPT_PERCENTAGE]),
        exempt_cap=float(company_data[EXEMPT_CAP]),
        accumulated_exemption=float(single_employee_data[ACCUMULATED_EXEMPTION]),
        exempts_periodicity=company_data[EXEMPTS_PERIODICITY],
        deductible_percentage=float(company_data[DEDUCTIBLE_PERCENTAGE]),
        deductible_cap=float(company_data[DEDUCTIBLE_CAP]),
        accumulated_deductible=float(single_employee_data[ACCUMULATED_DEDUCTIBLE]),
        voluntary_cap_percentage=float(company_data[VOLUNTARY_CAP_PERCENTAGE]),
        voluntary_cap=float(company_data[VOLUNTARY_CAP]),
        dependent=bool(int(single_employee_data[DEPENDENT])),
        dependent_cap=float(company_data[DEPENDENT_CAP]),
        dependent_percentage=float(company_data[DEPENDENT_PERCENTAGE])
    )
    return withholding_tax


def map_required_data_to_dict(targets_data: DictReader) -> dict:
    required_dict = dict()
    for row in targets_data:
        required_dict[row[DOCUMENT]] = int(row[TARGET_SALARY])
    return required_dict
