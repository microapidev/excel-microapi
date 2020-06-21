from rest_framework import serializers
from excel_api.models import Files


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = '__all__'
