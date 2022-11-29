from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MeterManagement, UsageRate, UnitRate, MeterReading


# Register your models here.

class MeterManagementAdmin(admin.ModelAdmin):
    list_display = ["country", "meter_type", "site_type"]
    list_filter = ["meter_type", "site_type", "country"]

class UsageRateAdmin(admin.ModelAdmin):
    list_display = ["eff_date"]

class UnitRateAdmin(admin.ModelAdmin):
    list_display = ["usage_rate", "meter", "units", "rate"]

class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ["date", "meter", "reader", "reading", "previous_reading", "usage", "cost"]

admin.site.register(MeterManagement,MeterManagementAdmin)
admin.site.register(UsageRate, UsageRateAdmin)
admin.site.register(UnitRate, UnitRateAdmin)
admin.site.register(MeterReading, MeterReadingAdmin)
