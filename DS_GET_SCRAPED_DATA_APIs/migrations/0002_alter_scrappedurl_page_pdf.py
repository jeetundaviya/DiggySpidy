# Generated by Django 4.1.3 on 2023-01-26 03:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DS_GET_SCRAPED_DATA_APIs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrappedurl',
            name='page_pdf',
            field=models.FileField(upload_to='DS_CORE/saved_data', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf'])]),
        ),
    ]
