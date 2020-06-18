from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import sys
import xlrd
import time
from excel_api.models import Files
from excel_api.serializers import FileSerializer
from rest_framework import generics
import pandas as pd

# Create your views here.
class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


@api_view(["GET", "POST"])
def parserview(request):
    start_time = time.time()
    workbook = xlrd.open_workbook(file_contents=request.FILES.get("FILE").read())
    worksheet = workbook.sheet_by_name("Sheet1")
    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    json_parsed = {"data": data, "process_time": total_time}

    return Response(json_parsed)
