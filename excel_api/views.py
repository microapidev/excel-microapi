import os
import pandas as pd
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import sys
import xlrd

from excel_api.models import Files
from excel_api.serializers import FileSerializer
from rest_framework import generics
from excel_api.excel_parser import get_file_name, start_timer
from excel_api.excel_parser import parse_excel_file, save_duplicates_excel
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .excel_handler import test_file
from .excel_handler import column_sum
from .excel_parser import print_duplicates

from django.core.files.storage import FileSystemStorage
import pythoncom
import win32com.client as win32
from openpyxl import load_workbook
from django.core.files.storage import FileSystemStorage
import pythoncom
import win32com.client as win32
from .Google import Create_Service
from django.http import JsonResponse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Create your views here.
# class FilesList(generics.ListCreateAPIView):
# # View to list all occurences of file
class FilesList(generics.ListAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


# View to add a new file
class FilesAdd(generics.CreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


@api_view(['POST'])
def parserview(request):
    file_obj = request.data.get('content')
    title = get_file_name(file_obj)
    result = parse_excel_file(file_obj)
    if result.get('data') is not None:
        file = Files.objects.create(title=title, content=file_obj)
        file.save()

    json_parsed = result
    return JsonResponse(json_parsed)


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
            file = request.FILES["excelfile"]
            fs = FileSystemStorage()
            fname = fs.save(file.name, file)
            sheetid = data.get('sheetid')
            sname = data.get('sheetname')
            estart = data.get('excelstartregion')
            gstart = data.get('googlesheetstartregion')
            if file.name == "":
                res_msg = {'msg': 'File Name is Needed'}
                return Response(res_msg, status=400)
                # messages.error(request, 'File Name is Needed')
                # return HttpResponseRedirect('export')
            if sheetid == "" or sname == "" or estart == "" or gstart == "":
                res_msg = {'msg': 'Please Enter all Fields'}
                return Response(res_msg, status=400)
                # messages.warning(request, 'Please Enter all Fields')
                # return HttpResponseRedirect('export')
            if not checkFile(file.name):
                res_msg = {'msg': 'File Extension not Supported'}
                return Response(res_msg, status=400)
                # messages.error(request, 'File Extension not Supported')
                # return HttpResponseRedirect('export')
            else:
                xlApp = win32.Dispatch('Excel.Application')
                wb = xlApp.Workbooks.Open(r""+os.getcwd()+"/media/"+fname)
                print(wb)
                try:
                    ws = wb.Worksheets(sname)
                except Exception as e:
                    res_msg = {'msg': 'Error opening worksheet '+ str(e)}
                    return Response(res_msg, status=400)
                    # messages.error(request, 'Error opening worksheet '+ str(e))
                    # return HttpResponseRedirect('export')
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
                    res_msg = {'msg': 'Error Uploading to google sheets: '+ str(e)}
                    return Response(res_msg, status=401)
                    # messages.warning(request, 'Error Uploading to google sheets: '+ str(e))
                    # return HttpResponseRedirect('export')
                
                res_msg = {'msg': 'Worksheet Succesfully exported to google sheets'}
                return Response(res_msg)
                # messages.success(request, 'Worksheet Succesfully exported to google sheets')
                # return HttpResponseRedirect('export')
    res_msg = {'msg': 'Please Upload a File First'}
    return Response(res_msg, status=400)

    #return render(request, 'index.html')

@csrf_exempt
def filesAdd(request):
    file_obj = request.data.get('content')
    title = get_file_name(file_obj)
    result = parse_excel_file(file_obj)
    if result.get('data') is not None:
        file = Files.objects.create(title=title, content=file_obj)
        file.save()
    
    json_parsed = result
    return JsonResponse(json_parsed)


@api_view(['POST'])
def search_file(request):
    column = request.data['column']
    file_obj = request.data.get('content')
    keyword = request.data['keyword']
    data = pd.read_excel(file_obj, sheet_name="Sheet1")
    try:
        present = data[column] == keyword
        if present is True:
            status = "True"
        else:
            status = "False"
        present = {"status":status}
    except KeyError:
        return JsonResponse({"status":"Column doesn't exist"})
    return JsonResponse(present,safe=False)


@api_view(['POST'])
def check_file(request):
    if request.method == 'POST':
        file_obj = request.data.get('content')
        test_result = test_file(file_obj)
        return JsonResponse(test_result, status=201, safe=False)

    else:
        message = "Access Denied, Use post method"
        return JsonResponse(message, status=400, safe=False)


@api_view(['POST'])
def modify_file(request):
    if request.method == 'POST':
        file = request.data.get('content')
        title = get_file_name(file)
        data = json.loads(request.data.get('data'))
        if title is None:
            print("No File Uploaded")
            return redirect(request.url)

        sheet = data['sheet']
        update = data['updated']

        wb = load_workbook(file)
        ws = wb.active
        ws.append(update)
       # textfile = "{}.xlsx".format(title)
        #updated_file = Files.objects.create(title=title, content=wb)
        wb.save(os.path.join(BASE_DIR, "media",title))
        #updated_file.save()

        return JsonResponse({"status":"Success"})
    return "success"


@csrf_exempt
@api_view(['POST'])
def process_duplicates(request):
        file_obj = request.data.get('content')
        duplicates = save_duplicates_excel(file_obj)
        print(duplicates)
        return Response(duplicates)

@csrf_exempt
@api_view(['POST'])
def print_duplicate(request):
        file_obj = request.data.get('content')
        new_col = print_duplicates(file_obj)
        print(new_col)
        return Response(new_col)




@api_view(['POST'])
def column_sum(request):
    if request.method == 'POST':

       file_obj = request.data.get('content')
#      sheet_name = request.data.get('sheet')
       column_num = request.data.get('column')

        # data = JSONParser().parse(request)
        # file_obj = data['path']
        # sheet_name = data['sheet']
        # column_name = data['column']

       sum_result = column_sum(file_obj, column_num)
       return JsonResponse(sum_result, status=201, safe=False)

    else:
        message = "Access Denied, Use post method"
        return JsonResponse(message, status=400, safe=False)
