from django.contrib import admin

from .models import *

class BillingAdmin(admin.ModelAdmin):
    list_display = ('meter','unit_rate','amount', 'is_paid', 'meter_reading')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_number', 'meter', 'meter_reading', 'amount', 'payment_date']
admin.site.register(Billing, BillingAdmin)
admin.site.register(Payment,PaymentAdmin)


