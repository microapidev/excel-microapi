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
