from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import MeterManagement, UsageRate, UnitRate, MeterReading, MeterMutation
from .models import *
from billing.models import Billing,Payment

class MeterTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'type_code']

class PricingCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category_name',
        'category_rate',
        'tax_rate',
        'category_number'
    ]

class ConcentratorAdmin(admin.ModelAdmin):
    list_display = [
        'concentrator_name',
        'concentrator_number',
        'company_name'
    ]
class PaymentInlineAdmin(admin.TabularInline):
    model = Payment
    fields = (
        'payment_number',
        'customer',
        'meter',
        'meter_reading',
        'amount',
        'payment_date',
    )
class MeterManagementAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "meter_code",
        "country",
        "site_type",
        "current_reading",
    ]
    list_filter = ["site_type", "country"]

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

    inlines = [PaymentInlineAdmin]

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
admin.site.register(MeterTypes, MeterTypeAdmin)
admin.site.register(PricingCategory, PricingCategoryAdmin)
admin.site.register(Concentrator, ConcentratorAdmin)