# Generated by Django 4.2.11 on 2024-03-10 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtractedPDFData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to='uploaded_files/')),
                ('folder_path', models.CharField(max_length=255)),
                ('output_path', models.CharField(max_length=255)),
            ],
        ),
    ]