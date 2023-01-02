# Generated by Django 3.2.7 on 2023-01-01 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0012_auto_20230101_0346'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MeterType',
            new_name='MeterTypes',
        ),
        migrations.AddField(
            model_name='metermanagement',
            name='meter_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='meters.metertypes'),
        ),
    ]