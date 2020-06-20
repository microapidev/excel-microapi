<<<<<<< HEAD
import os

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import sys
import xlrd
from excel_api.models import Files
from excel_api.serializers import FileSerializer
from rest_framework import generics
from django.conf import settings


from excel_api.excel_parser import get_duplicates_excel
@api_view(['GET'])
def get_duplicates(request):
    media_root = settings.MEDIA_ROOT
    file_name = request.GET.get("file_name")
    media_root += f'\\files\{file_name}'
    result = get_duplicates_excel(media_root)
    return Response(result)



# Create your views here.
class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


@api_view(['GET', 'POST'])
def parserview(request):
    start_time = start_timer()

    title = get_file_name(request.data.get('content'))
    file = Files.objects.get(title=title)
    content = file.content.url
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), content)
    workbook = xlrd.open_workbook("."+filepath)
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

    
    
=======
import os
import pandas as pd
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import sys
import xlrd
from excel_api.models import Files
from excel_api.serializers import FileSerializer
from rest_framework import generics
from excel_api.excel_parser import get_file_name, start_timer, parse_excel_file
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .excel_handler import test_file
from .excel_handler import column_sum

from django.core.files.storage import FileSystemStorage
# import pythoncom
# import win32com.client as win32
from .Google import Create_Service
from django.http import JsonResponse


# Create your views here.
# View to list all occurences of file
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

# @api_view(['POST'])
# def column_sum(request):
#     if request.method == 'POST':
#
#         file_obj = request.data.get('content')
#         sheet_name = request.data.get('sheet')
#         column_name = request.data.get('column')
#
#         sum_result = column_sum(file_obj, sheet_name, column_name)
#         return JsonResponse(sum_result, status=201, safe=False)
#
#     else:
#         message = "Access Denied, Use post method"
#         return JsonResponse(message, status=400, safe=False)
>>>>>>> 4853b7279337d750fedfae6d32b9839df497ff46
