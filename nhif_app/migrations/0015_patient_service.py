# Generated by Django 5.0.7 on 2024-10-11 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0014_patient_renaldialysisrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='service',
            field=models.CharField(default='Dialysis', max_length=100),
        ),
    ]
