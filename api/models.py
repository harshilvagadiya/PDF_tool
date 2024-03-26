from django.db import models

# Create your models here.
class ExtractedPDFData(models.Model):
    uploaded_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)
    folder_path = models.CharField(max_length=255)
    output_path = models.CharField(max_length=255)

    def __str__(self):
        return self.folder_path