# Generated by Django 5.0.6 on 2024-07-27 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0005_remove_nhifclaim_secondary_status_nhifclaim_done'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhifclaim',
            name='dr_code',
            field=models.CharField(choices=[('none', '-----'), ('kariuki', 'A4157'), ('mugendi', 'A5027'), ('chira', 'A3655')], default='none', max_length=20),
        ),
    ]
