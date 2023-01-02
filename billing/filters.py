from django_filters.rest_framework import FilterSet
from .models import Payment

class PaymentFilter(FilterSet):
    class Meta:
        model = Payment
        fields = {
            'meter':['exact'],
            
        }