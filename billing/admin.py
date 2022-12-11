from django.contrib import admin

from .models import *

class BillingAdmin(admin.ModelAdmin):
    list_display = ('meter','unit_rate','amount', 'is_paid', 'meter_reading')

admin.site.register(Billing, BillingAdmin)
admin.site.register(Payment)


