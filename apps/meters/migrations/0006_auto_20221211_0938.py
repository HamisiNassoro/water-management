# Generated by Django 3.2.7 on 2022-12-11 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0005_alter_metermanagement_meter_reading'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeterTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='metermanagement',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='meters.metertypes'),
        ),
    ]
