import csv
from .serializers import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from v1_process.services.gross_up_service import GrossUpService
from v1_process.services.social_security_service import SocialSecurityService
from v1_process.services.withholding_tax_service import WithholdingTaxService


# Create your views here.

@csrf_exempt
def exec_excel_pipeline(request):
    if(request.method == 'POST'):
        
        file = request.FILES['file'] 
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            print(row)

        """
        Populate with data from the serialization
        It should be a list of objects to inject to the services layer
        """
        ss_service = SocialSecurityService(100000, 8004084)
        wt_service = WithholdingTaxService(True, 0)
        
        #This service should be used only for excecution of the main process, and the rest of the logic should live within the GrossUpService
        gross_up_service = GrossUpService(ss_service, wt_service)
        
        return_csv = gross_up_service.exec()
        
        
        """data = JSONParser().parse(request)
        serialized = WithholdingTaxSerializer(data=data)
        if serialized.is_valid():
            print('funcional', serialized.data.get('is_foreigner'))
        else:
            print('Error in serialization')"""
    
    return HttpResponse(return_csv)

@csrf_exempt
def exec_database_pipeline(request):
    return HttpResponse('Database call')