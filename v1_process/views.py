import csv
from .serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from v1_process.utils.csv_loader import load_company_employees_data, map_required_data_to_dict
from rest_framework.parsers import JSONParser

from v1_process.services.gross_up_service import GrossUpService
from v1_process.dictionaries.dictionary import COMPANY_NIT
from v1_process.utils.csv_mapper import map_output_csv_to_return_data
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.services.withholding_tax_service import WithholdingTaxService


# Create your views here.

@csrf_exempt
def exec_excel_pipeline(request):

    response = HttpResponse()

    if request.method == 'POST':

        company_data = request.FILES['company_data']
        employee_data = request.FILES['employee_data']
        required_data = request.FILES['required_data']

        decoded_company_data = company_data.read().decode('utf-8').splitlines()
        decoded_employee_data = employee_data.read().decode('utf-8').splitlines()
        decoded_required_data = required_data.read().decode('utf-8').splitlines()

        reader_company_data = csv.DictReader(decoded_company_data)
        reader_employee_data = csv.DictReader(decoded_employee_data)
        reader_required_data = csv.DictReader(decoded_required_data)

        required_dict = map_required_data_to_dict(reader_required_data)
        single_company_data = next(reader_company_data)

        employees = load_company_employees_data(single_company_data, reader_employee_data, required_dict)

        gross_up_service = GrossUpService(employees, single_company_data[COMPANY_NIT])
        file_name = gross_up_service.exec()
        file_data = map_output_csv_to_return_data(file_name)

        response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response

@csrf_exempt
def exec_database_pipeline(request):
    return HttpResponse('Database call')