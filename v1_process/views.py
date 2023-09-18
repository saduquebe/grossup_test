import csv
from .serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from v1_process.utils.csv_loader import load_company_employees_data, map_required_data_to_dict
from rest_framework.parsers import JSONParser

from v1_process.services.gross_up_service import GrossUpService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.services.withholding_tax_service import WithholdingTaxService


# Create your views here.

@csrf_exempt
def exec_excel_pipeline(request):
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

        employees = load_company_employees_data(reader_company_data, reader_employee_data, required_dict)

        gross_up_service = GrossUpService(employees)
        gross_up_service.exec()

    return HttpResponse()

@csrf_exempt
def exec_database_pipeline(request):
    return HttpResponse('Database call')