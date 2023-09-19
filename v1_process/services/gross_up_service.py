"""
Fill this service with   
"""
from v1_process.services.withholding_tax_service import WithholdingTaxService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.models import SocialSecurity, Employee, WithholdingTax
from v1_process.dictionaries.table import ranges
from v1_process.utils.calculate_base_salary import calculate_base_salary
from copy import deepcopy


class GrossUpService:
    _clearance_allowed: int = 100

    def __init__(self, employees: list):
        self.employees = employees
        self.social_security_service = SocialSecurityService()
        self.withholding_tax_service = WithholdingTaxService()

    def _gross_up(
            self, employee: Employee,
    ):
        final_gross_up: int = 0
        final_employee = deepcopy(employee)

        base_salary = calculate_base_salary(
            employee, self.social_security_service, self.withholding_tax_service
        )

        # First stage of the binary search
        while base_salary < employee.target_salary:

            if final_gross_up != 0:
                # Increment the gross up exponentially
                final_gross_up += final_gross_up
            else:
                final_gross_up = base_salary

            # The gross up is added to social security
            final_employee.social_security.wage_income = (
                    employee.social_security.wage_income + final_gross_up
            )
            social_security_values = self.social_security_service.exec(
                final_employee.social_security, ranges)

            # The gross up is added to withholding tax
            final_employee.withholding_tax.social_security_values = \
                social_security_values

            final_employee.withholding_tax.gross_total_incomes = (
                    employee.withholding_tax.gross_total_incomes + final_gross_up
            )
            # Recalculates the base salary
            base_salary = calculate_base_salary(
                final_employee, self.social_security_service,
                self.withholding_tax_service
            )
        top = final_gross_up
        bottom = 0

        while (
                abs(employee.target_salary - base_salary) > self._clearance_allowed
        ):
            final_gross_up = (top + bottom) // 2

            # The gross up is added to social security
            final_employee.social_security.wage_income = (
                    employee.social_security.wage_income + final_gross_up
            )
            social_security_values = self.social_security_service.exec(
                final_employee.social_security, ranges)

            # The gross up is added to withholding tax
            final_employee.withholding_tax.social_security_values = \
                social_security_values

            final_employee.withholding_tax.gross_total_incomes = (
                    employee.withholding_tax.gross_total_incomes + final_gross_up
            )

            # Recalculates the base salary
            base_salary = calculate_base_salary(
                final_employee, self.social_security_service,
                self.withholding_tax_service
            )

            if base_salary < employee.target_salary:
                bottom = final_gross_up
            else:
                top = final_gross_up

        return final_gross_up

    def exec(self) -> str:
        for employee in self.employees:
            gross_up = self._gross_up(employee)
            print("-------------")
            print(gross_up)

    def _save_to_database(self):
        # Logic to connect to Model class and persist data
        return
