# Generated by Django 3.2.7 on 2022-12-11 07:05

import base.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0006_auto_20221211_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='metermanagement',
            name='meter_code',
            field=base.fields.SUBField(blank=True, max_length=10, null=True),
        ),
    ]
