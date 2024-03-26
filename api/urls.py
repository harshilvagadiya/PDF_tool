from django.contrib import admin
from django.urls import path
from .views import ExtractPDFDataView
urlpatterns = [
    path('tool/', ExtractPDFDataView.as_view(), name='extract_pdf_data'),
]
