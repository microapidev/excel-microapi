import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseRedirect
import json
import sys
import xlrd
from excel_api.models import Files
from excel_api.serializers import FileSerializer
from rest_framework import generics
import pythoncom
import win32com.client as win32
from .Google import Create_Service
from excel_api.excel_parser import get_file_name, start_timer
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .excel_handler import test_file
from .excel_handler import column_sum


# Create your views here.
# View to list all occurences of file
class FilesList(generics.ListAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer

# View to add a new file
class FilesAdd(generics.CreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


@api_view(['GET', 'POST'])
def parserview(request):
    start_time = start_timer()
    #title = get_file_name(request.data.get('content'))
    title = request.data.get('title')
    file = Files.objects.get(title=title)
    content = file.content.url
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), content)
    workbook = xlrd.open_workbook("." + filepath)
    worksheet = workbook.sheet_by_name('Sheet1')
    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)
    end_time = start_timer()
    total_time = round(end_time - start_time, 2)
    json_parsed = {'data': data, 'process_time': total_time}

    return Response(json_parsed)

  FILE_EXT = ["XLS", "XLSX"]

def checkFile(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in FILE_EXT:
        return True
    else:
        return False

@api_view(['GET', 'POST'])
def export(request):

    pythoncom.CoInitialize()
    context = {}
    if request.method == "POST":
        xlApp = win32.Dispatch('Excel.Application')
        if request.FILES:
            data = request.POST.copy()
            file = request.FILES["excel"]
            fs = FileSystemStorage()
            fname = fs.save(file.name, file)
            sheetid = data.get('sheetid')
            sname = data.get('sheetname')
            estart = data.get('estart')
            gstart = data.get('gstart')
            if file.name == "":
                messages.error(request, 'File Name is Needed')
                return HttpResponseRedirect('export')
            if sheetid == "" or sname == "" or estart == "" or gstart == "":
                messages.warning(request, 'Please Enter all Fields')
                return HttpResponseRedirect('export')
            if not checkFile(file.name):
                messages.error(request, 'File Extension not Supported')
                return HttpResponseRedirect('export')
            else:
                xlApp = win32.Dispatch('Excel.Application')
                wb = xlApp.Workbooks.Open(r""+os.getcwd()+"/media/"+fname)
                print(wb)
                try:
                    ws = wb.Worksheets(sname)
                except Exception as e:
                    messages.error(request, 'Error opening worksheet '+ str(e))
                    return HttpResponseRedirect('export')
                rngData = ws.Range(estart).CurrentRegion()

                #191h4mt1-iSzIdeRdbszAcWaV_m7_gbierp_bLImnWnI
                gsheet_id = sheetid
                CLIENT_SECRET_FILE = ''+os.getcwd()+'/client_token.json'
                API_SERVICE_NAME = 'sheets'
                API_VERSION = 'v4'
                SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
                service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

                try:
                    response = service.spreadsheets().values().append(
                        spreadsheetId=gsheet_id,
                        valueInputOption='RAW',
                        range='data!'+gstart,
                        body=dict(
                            majorDimension='ROWS',
                            values=rngData
                        )
                    ).execute()                    
                except Exception as e:
                    messages.warning(request, 'Error Uploading to google sheets: '+ str(e))
                    return HttpResponseRedirect('export')

                messages.success(request, 'Worksheet Succesfully exported to google sheets')
                return HttpResponseRedirect('export')

    return render(request, 'index.html')

@csrf_exempt
def check_file(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        path_value = data['path']
        test_result = test_file(path_value)
        return JsonResponse(test_result, status=201, safe=False)


    else:
        message = "Access Denied, Use post method"
        return JsonResponse(message, status=400, safe=False)
    
    
@csrf_exempt
def column_sum(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        path_value = data['path']
        sheet_name = data['sheet']
        column_name = data['column']
        
        sum_result = column_sum(path_value, sheet_name, column_name)
        return JsonResponse(sum_result, status=201, safe=False)


    else:
        message = "Access Denied, Use post method"
        return JsonResponse(message, status=400, safe=False)
