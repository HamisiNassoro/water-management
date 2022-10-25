from django.contrib import admin

from .models import MeterManagement


# Register your models here.

class MeterManagementAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "meter_type", "site_type"]
    list_filter = ["meter_type", "site_type", "country"]

admin.site.register(MeterManagement,MeterManagementAdmin)
