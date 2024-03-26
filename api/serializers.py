from rest_framework import serializers
from .models import ExtractedPDFData

class ExtractedPDFDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedPDFData
        fields = '__all__'
