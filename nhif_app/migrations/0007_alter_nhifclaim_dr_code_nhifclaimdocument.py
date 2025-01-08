# Generated by Django 5.0.6 on 2024-07-27 07:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nhif_app', '0006_alter_nhifclaim_dr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nhifclaim',
            name='dr_code',
            field=models.CharField(choices=[('A4157', 'Kariuki'), ('A5027', 'Mugendi'), ('A3655', 'Chira'), ('A14254', 'Akampa'), ('013033', 'Adong'), ('A7642', 'Kaguongo'), ('A4653', 'Nderitu'), ('A6843', 'Amandi'), ('A7489', 'Laichena'), ('A10231', 'Okendi'), ('A6253', 'Sung'), ('A9479', 'Naomi'), ('A8245', 'Mutiso'), ('A9347', 'Milo')], default='none', max_length=20),
        ),
        migrations.CreateModel(
            name='NHIFClaimDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_name', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to='nhif_documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='nhif_app.nhifclaim')),
            ],
        ),
    ]
