# Generated by Django 5.0.6 on 2024-07-25 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0002_nhifclaim_dr_code_alter_nhifclaim_procedure'),
    ]

    operations = [
        migrations.AddField(
            model_name='nhifclaim',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
