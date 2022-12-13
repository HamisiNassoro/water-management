from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MeterManagement, UsageRate, UnitRate, MeterReading, MeterMutation

from billing.models import Billing
class BillsInlineAdmin(admin.TabularInline):
    model = Billing
    fields = ('unit_rate', 'is_paid',)
class MeterManagementAdmin(admin.ModelAdmin):
    list_display = ["meter_code", "country", "meter_type", "site_type",]
    list_filter = ["meter_type", "site_type", "country"]

    readonly_fields = (
        'meter_code',
    )
    """fieldsets = (
        (None,{
            "fields":(
                'meter_code',
            )
            
        }),
    )"""

    inlines = [BillsInlineAdmin]

class UsageRateAdmin(admin.ModelAdmin):
    list_display = ["eff_date"]

class UnitRateAdmin(admin.ModelAdmin):
    list_display = ["usage_rate", "meter", "units", "rate"]

class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ["date", "meter", "reader", "reading", "previous_reading", "usage", "cost"]

class MeterMutationAdmin(admin.ModelAdmin):
    list_display = ['id', 'meter', 'start_reading', 'timestamp', 'litre_usage', 'end_reading']

admin.site.register(MeterManagement,MeterManagementAdmin)
admin.site.register(UsageRate, UsageRateAdmin)
admin.site.register(UnitRate, UnitRateAdmin)
admin.site.register(MeterReading, MeterReadingAdmin)
admin.site.register(MeterMutation, MeterMutationAdmin)
