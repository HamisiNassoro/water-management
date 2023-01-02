from django_filters.rest_framework import FilterSet
from .models import MeterManagement

class MeterFilter(FilterSet):
    class Meta:
        model = MeterManagement
        fields = {
            'pricing_category':['exact'],
            'meter_type': ['exact']
        }