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
from excel_api.excel_parser import get_file_name, start_timer


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
