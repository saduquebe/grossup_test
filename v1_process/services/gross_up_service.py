"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import Employee, GrossUp
from v1_process.dictionaries.table import ranges
from copy import deepcopy
from v1_process.utils.csv_mapper import map_gross_up_to_csv


class GrossUpService:
    _clearance_allowed: int = 100

    def __init__(self, employees: list[Employee], company_nit: str):
        self.employees = employees
        self.social_security_service = SocialSecurityService()
        self.withholding_tax_service = WithholdingTaxService()
        self.company_nit = company_nit

    def _calculate_net_salary(self,
                              employee: Employee
                              ) -> int:

        social_security_values = self.social_security_service.exec(
            employee.social_security, ranges)

        employee.withholding_tax.social_security_values = social_security_values

        withholding_tax_contribution = self.withholding_tax_service.exec(
            employee.withholding_tax)

        base = employee.social_security.wage_income

        return (
                base - sum(social_security_values.values()) -
                withholding_tax_contribution
        )

    def _first_binary_search_stage(
            self, employee: Employee
    ):

        employee_copy = deepcopy(employee)

        net_salary = self._calculate_net_salary(employee)

        top = net_salary
        while net_salary < employee.target_salary:
            # Increment the gross up exponentially
            top += top

            # The gross up is added to social security
            employee_copy.social_security.wage_income = (
                    employee.social_security.wage_income + top
            )
            social_security_values = self.social_security_service.exec(
                employee_copy.social_security, ranges)

            # The gross up is added to withholding tax
            employee_copy.withholding_tax.social_security_values = \
                social_security_values

            employee_copy.withholding_tax.gross_total_incomes = (
                    employee.withholding_tax.gross_total_incomes +
                    top
            )
            # Recalculates the net salary
            net_salary = self._calculate_net_salary(employee_copy)
        return top

    def _second_binary_search_stage(
            self, employee: Employee, top: int, bottom: int
    ):

        employee_copy = deepcopy(employee)
        net_salary = self._calculate_net_salary(employee)
        final_gross_up: int = 0
        while (
                abs(employee.target_salary - net_salary) >
                self._clearance_allowed
        ):
            final_gross_up = (top + bottom) // 2

            # The gross up is added to social security
            employee_copy.social_security.wage_income = (
                    employee.social_security.wage_income + final_gross_up
            )
            social_security_values = self.social_security_service.exec(
                employee_copy.social_security, ranges)

            # The gross up is added to withholding tax
            employee_copy.withholding_tax.social_security_values = \
                social_security_values

            employee_copy.withholding_tax.gross_total_incomes = (
                    employee.withholding_tax.gross_total_incomes +
                    final_gross_up
            )

            # Recalculates the net salary
            net_salary = self._calculate_net_salary(employee_copy)

            if net_salary < employee.target_salary:
                bottom = final_gross_up
            else:
                top = final_gross_up
        return final_gross_up

    def _gross_up(
            self, employee: Employee,
    ):
        # First stage of the binary search
        top = self._first_binary_search_stage(employee)
        bottom = 0
        final_gross_up = self._second_binary_search_stage(employee, top, bottom)

        return final_gross_up

    def exec(self) -> str:

        gross_up_list = []
        for employee in self.employees:
            gross_up = self._gross_up(employee)
            gross_up_list.append(GrossUp(employee.document, gross_up))

        return map_gross_up_to_csv(gross_up_list, self.company_nit, self.employees[0].withholding_tax.payroll_date)

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
