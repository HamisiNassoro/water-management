# Generated by Django 3.2.7 on 2023-01-01 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0011_metermanagement_current_reading'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concentrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concentrator_name', models.CharField(blank=True, max_length=200, null=True)),
                ('concentrator_number', models.CharField(blank=True, max_length=200, null=True)),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Concentrator',
                'verbose_name_plural': 'Concentrators',
            },
        ),
        migrations.CreateModel(
            name='MeterType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(blank=True, max_length=100, null=True)),
                ('type_code', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Meter Type',
                'verbose_name_plural': 'Meter Types',
            },
        ),
        migrations.CreateModel(
            name='PricingCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(blank=True, max_length=200, null=True)),
                ('category_rate', models.DecimalField(decimal_places=4, max_digits=8)),
                ('category_number', models.CharField(blank=True, max_length=200, null=True)),
                ('tax_rate', models.DecimalField(decimal_places=4, max_digits=8)),
            ],
            options={
                'verbose_name': 'Pricing Category',
                'verbose_name_plural': 'Pricing Categories',
            },
        ),
        migrations.RemoveField(
            model_name='metermanagement',
            name='meter_type',
        ),
        migrations.RemoveField(
            model_name='metermanagement',
            name='type',
        ),
        migrations.DeleteModel(
            name='MeterTypes',
        ),
        migrations.AddField(
            model_name='metermanagement',
            name='concentrator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='meters.concentrator'),
        ),
    ]
