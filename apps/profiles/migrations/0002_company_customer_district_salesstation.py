# Generated by Django 3.2.7 on 2023-01-01 00:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200, null=True)),
                ('company_number', models.CharField(blank=True, max_length=200, null=True)),
                ('company_description', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district_name', models.CharField(blank=True, max_length=200, null=True)),
                ('district_description', models.CharField(blank=True, max_length=200, null=True)),
                ('district_number', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.company')),
            ],
            options={
                'verbose_name': 'District',
                'verbose_name_plural': 'Districts',
            },
        ),
        migrations.CreateModel(
            name='SalesStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_name', models.CharField(blank=True, max_length=200, null=True)),
                ('station_number', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.company')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.district')),
            ],
            options={
                'verbose_name': 'Sales Station',
                'verbose_name_plural': 'Sales Stations',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_number', models.CharField(blank=True, max_length=200, null=True)),
                ('account_id', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_address', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_phone', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_email', models.CharField(blank=True, max_length=200, null=True)),
                ('price_categories', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_id', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_type', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.company')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
    ]
