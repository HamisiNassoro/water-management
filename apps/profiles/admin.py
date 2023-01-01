from django.contrib import admin

from .models import *

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "gender", "phone_number", "country", "city"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "pkid", "user"]


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company_number', 'company_description']
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['district_name', 'company', 'district_description', 'district_number']

class SalesStationAdmin(admin.ModelAdmin):
    list_display = ['station_name', 'district', 'company', 'station_number']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_number', 'customer_address', 'meter_id']


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Company, CompanyAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(SalesStation, SalesStationAdmin)
admin.site.register(Customer, CustomerAdmin)
