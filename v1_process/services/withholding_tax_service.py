"""
Define if these are methods or functions (instance related or not) to define a class
"""
import v1_process.dictionaries.table as tb
from v1_process.models import WithholdingTax
from v1_process.dictionaries.dictionary import *

def get_worked_days(payroll_date, initial_date_contract, final_date_contract):
    payroll_date_splited = payroll_date.split('-')
    initial_date_splited = initial_date_contract.split('-')
    final_date_splited = final_date_contract.split('-')

    if (
            int(payroll_date_splited[0]) == int(initial_date_splited[0])
            and int(payroll_date_splited[1]) == int(initial_date_splited[1])
    ):
        return 30 - int(initial_date_splited[2])

    if (
            int(payroll_date_splited[0]) == int(final_date_splited[0])
            and int(payroll_date_splited[1]) == int(final_date_splited[1])
    ):
        return int(final_date_splited[2])

    return 30


def project(value, procedure_type, worked_days):
    if procedure_type == "T":
        return (value / worked_days) * 30
    return value


def evaluate_cap(value, cap):
    if value > cap:
        return cap
    return value


def get_table_value(base, table, uvt_value):
    for rank in table:
        if rank["min"] * uvt_value < base and base < rank["max"] * uvt_value:
            return (
                    (base - rank["subsValue"] * uvt_value) * rank["percentage"] +
                    rank["addValue"] * uvt_value
            )
    last_rank = table[len(table) - 1]
    return (
            (base - last_rank["subsValue"] * uvt_value) * last_rank["percentage"] +
            last_rank["addValue"] * uvt_value
    )


def calculate_month_withholding_tax_value(
        base, procedure_type, argument, uvt_value, worked_days
):
    if procedure_type == "T":
        return (get_table_value(base, argument, uvt_value) / 30) * worked_days
    else:
        return base * argument


def calculate_non_constitutive_incomes(
        non_constitutive_incomes_cap, minimum_month_salary, social_security_values,
        procedure_type, worked_days
):
    total_social_security_values = (
            social_security_values[HEALTH_CONTRIBUTION]
            + social_security_values[RETIRE_CONTRIBUTION]
            + social_security_values[SOLIDARITY_CONTRIBUTION]
            + social_security_values[VOLUNTARY_MANDATORY_PENSION_CONTRIBUTION]
    )

    total_social_security_values_projected = project(
        total_social_security_values, procedure_type, worked_days
    )

    return evaluate_cap(
        total_social_security_values_projected,
        non_constitutive_incomes_cap * minimum_month_salary
    )

# At 2023 this function gets the exemption value of 25%(Tope 25%)
def get_exemption(
    periodicity, gross_exempt, total_reliefs, voluntary_withholding,
    exempt_percentage, annual_exempt_cap, accumulated_exemption, uvt_value
):
    month_exemption = (
        gross_exempt - total_reliefs - voluntary_withholding
    ) * exempt_percentage
    cap_pesos = annual_exempt_cap * uvt_value
    if periodicity == "A":
        remainder = cap_pesos - accumulated_exemption
        if remainder <= 0:
            return 0
        return evaluate_cap(month_exemption, remainder)
    else:
        monthly_cap = annual_exempt_cap / 12
        return evaluate_cap(month_exemption, monthly_cap)

# At 2023 this function gets the deductible value of 40%(Tope 40%)
def get_deductible(
    periodicity, gross_exempt, deductible_percentage,
    annual_deductible_cap, accumulated_deductible, uvt_value
):
    month_deductible = gross_exempt * deductible_percentage
    cap_pesos = annual_deductible_cap * uvt_value
    if periodicity == "A":
        remainder = cap_pesos - accumulated_deductible
        if remainder <= 0:
            return 0
        return evaluate_cap(month_deductible, remainder)
    else:
        monthly_cap = annual_deductible_cap / 12
        return evaluate_cap(month_deductible, monthly_cap)


"""
Service to access namespace 
Fill this service with a list of WithholdingTax objects 
"""


class WithholdingTaxService:

    def exec(self, withholding_tax: WithholdingTax) -> float:
        # Calculate the working days by the contract
        worked_days = get_worked_days(
            withholding_tax.payroll_date,
            withholding_tax.initial_date_contract,
            withholding_tax.final_date_contract
        )
        # Project the total incomes
        total_incomes = project(
            withholding_tax.gross_total_incomes,
            withholding_tax.procedure_type,
            worked_days
        )

        # If the employee is a foreigner, the withholding tax value is different
        if withholding_tax.is_foreigner:
            return total_incomes * withholding_tax.percentage_foreigner

        # Calculate the final voluntary withholding cap
        final_voluntary_withholding_cap = evaluate_cap(
            total_incomes * withholding_tax.voluntary_cap_percentage,
            withholding_tax.voluntary_cap * withholding_tax.uvt_value
        )

        # Calculate the final voluntary withholding
        voluntary_withholding_projected = project(
            withholding_tax.gross_voluntary_withholding,
            withholding_tax.procedure_type,
            worked_days
        )

        voluntary_withholding = evaluate_cap(
            voluntary_withholding_projected, final_voluntary_withholding_cap
        )

        # Calculate the non-constitutive incomes (ingresos no constitutivos de
        # renta)
        non_constitutive_incomes = calculate_non_constitutive_incomes(
            withholding_tax.non_constitutive_incomes_cap,
            withholding_tax.minimum_month_salary,
            withholding_tax.social_security_values,
            withholding_tax.procedure_type,
            worked_days
        )

        # Calculate the gross exempt (renta bruta exenta)
        gross_exempt = (
                total_incomes - non_constitutive_incomes +
                withholding_tax.food_bonus
        )

        # Calculate the housing and health reliefs (Alivios de vivienda y salud)
        final_housing_relief = evaluate_cap(
            withholding_tax.housing_relief,
            withholding_tax.housing_relief_cap * withholding_tax.uvt_value
        )
        final_health_relief = evaluate_cap(
            withholding_tax.health_relief,
            withholding_tax.health_relief_cap * withholding_tax.uvt_value
        )

        # Calculate the dependent relief
        dependent_relief = 0
        if withholding_tax.dependent:
            weighted_dependent_relief = (
                    withholding_tax.dependent_sum *
                    withholding_tax.dependent_percentage
            )
            dependent_relief_projected = project(
                weighted_dependent_relief,
                withholding_tax.procedure_type,
                worked_days
            )
            dependent_relief = evaluate_cap(
                dependent_relief_projected,
                withholding_tax.dependent_cap * withholding_tax.uvt_value
            )

        # Calculate the total value of the reliefs
        total_reliefs = final_housing_relief + (
                final_health_relief + dependent_relief
        )

        # Calculate the gross cap exemption (Cap 25%)
        gross_cap_exemption = get_exemption(
            withholding_tax.exempts_periodicity,
            gross_exempt,
            total_reliefs,
            voluntary_withholding,
            withholding_tax.exempt_percentage,
            withholding_tax.exempt_cap,
            withholding_tax.accumulated_exemption,
            withholding_tax.uvt_value
        ) + voluntary_withholding

        # Calculate the gross cap deductible (Cap 40%)
        gross_cap_exemption_2 = get_deductible(
            withholding_tax.exempts_periodicity,
            gross_exempt,
            withholding_tax.deductible_percentage,
            withholding_tax.deductible_cap,
            withholding_tax.accumulated_deductible,
            withholding_tax.uvt_value
        )

        # Calculate the withholding base
        withholding_base = gross_exempt - min(gross_cap_exemption,
                                              gross_cap_exemption_2)

        # Calculate the monthly withholding tax
        monthly_withholding = 0
        if withholding_tax.procedure_type == "P":
            monthly_withholding = calculate_month_withholding_tax_value(
                withholding_base,
                withholding_tax.procedure_type,
                withholding_tax.argument_procedure_type,
                withholding_tax.uvt_value,
                worked_days
            )
        else:
            monthly_withholding = calculate_month_withholding_tax_value(
                withholding_base,
                withholding_tax.procedure_type,
                tb.uvtTable,
                withholding_tax.uvt_value,
                worked_days
            )

        return monthly_withholding

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
