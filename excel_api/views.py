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
from excel_api.excel_parser import get_file_name, start_timer, parse_excel_file


# Create your views here.
class FilesList(generics.ListCreateAPIView):
    queryset = Files.objects.all()
    serializer_class = FileSerializer


@api_view(['GET', 'POST'])
def parserview(request):
    title = get_file_name(request.data.get('content'))
    file = Files.objects.get(title=title)
    content = file.content.url
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), content)
    data = parse_excel_file(file)
    json_parsed = data


    return Response(json_parsed)
