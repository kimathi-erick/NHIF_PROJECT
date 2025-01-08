# Generated by Django 5.0.7 on 2024-10-14 14:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0015_patient_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='member_number',
            new_name='shifnumber',
        ),
        migrations.AddField(
            model_name='patient',
            name='facility_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='idnumber',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='phone',
            field=models.CharField(default=' ', max_length=15),
            preserve_default=False,
        ),
    ]
