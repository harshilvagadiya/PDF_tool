import os
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .utils import extract_data_from_pdf
from .models import ExtractedPDFData
from .serializers import ExtractedPDFDataSerializer
import pandas as pd
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ExtractPDFDataView(APIView):
    def post(self, request, format=None):
        logger.info("ExtractPDFDataView POST request received")

        folder_path = request.data.get('folder_path')
        output_path = request.data.get('output_path')
        uploaded_file = request.FILES.getlist('uploaded_file')
        
        logger.debug("Folder path: %s", folder_path)
        logger.debug("Output path: %s", output_path)
        logger.debug("Uploaded files: %s", uploaded_file)

        temp_folder = os.path.join(settings.MEDIA_ROOT, 'temp')
        uploaded_file_path = None

        try:
            # if uploaded_file:
            #     uploaded_file_path = os.path.join(temp_folder, uploaded_file.name)
            #     with open(uploaded_file_path, 'wb') as file:
            #         for chunk in uploaded_file.chunks():
            #             file.write(chunk)
            for uploaded_file in uploaded_file:
                uploaded_file_path = os.path.join(temp_folder, uploaded_file.name)
                with open(uploaded_file_path, 'wb') as file:
                    for chunk in uploaded_file.chunks():
                        file.write(chunk)
        except Exception as upload_error:
            logger.error("Error handling uploaded file: %s", str(upload_error))
            return Response({'error': f'Error handling uploaded file: {str(upload_error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        pdf_data = {}
        try:
            if folder_path:
                if not os.path.exists(folder_path):
                    logger.error("Folder does not exist: %s", folder_path)
                    return Response({'error': f'Folder does not exist: {folder_path}'}, status=status.HTTP_400_BAD_REQUEST)
                for filename in os.listdir(folder_path):
                    if filename.endswith(".pdf"):
                        pdf_path = os.path.join(folder_path, filename)
                        data = extract_data_from_pdf(pdf_path)
                        pdf_data[filename] = data
            elif uploaded_file_path:
                data = extract_data_from_pdf(uploaded_file_path)
                pdf_data[uploaded_file.name] = data
        except Exception as extraction_error:
            logger.error("Error extracting PDF data: %s", str(extraction_error))
            return Response({'error': f'Error extracting PDF data: {str(extraction_error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        df = pd.DataFrame.from_dict(pdf_data, orient='index')

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file_name = f"extracted_data_{current_datetime}.xlsx"

        try:
            if output_path:
                excel_file_path = os.path.join(output_path, excel_file_name)
            elif folder_path:
                excel_file_path = os.path.join(folder_path, excel_file_name)
            else:
                excel_file_path = os.path.join(temp_folder, excel_file_name)

            df.to_excel(excel_file_path)
            logger.info("Excel file saved successfully: %s", excel_file_path)
        except Exception as excel_error:
            logger.error("Error saving Excel file: %s", str(excel_error))
            return Response({'error': f'Error saving Excel file: {str(excel_error)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            if uploaded_file_path:
                os.remove(uploaded_file_path)
                logger.debug("Uploaded file removed: %s", uploaded_file_path)

        logger.info("Data extraction and export completed successfully")
        logger.info("\n\n--------DONE--------\n")
        return Response({'success': f'Data has been exported to {excel_file_path}'}, status=status.HTTP_200_OK)
