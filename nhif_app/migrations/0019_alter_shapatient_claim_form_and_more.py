# Generated by Django 5.0.7 on 2024-11-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0018_shapatient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shapatient',
            name='claim_form',
            field=models.FileField(upload_to='claims/'),
        ),
        migrations.AlterField(
            model_name='shapatient',
            name='full_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='shapatient',
            name='inpatient_number',
            field=models.CharField(max_length=255),
        ),
    ]
