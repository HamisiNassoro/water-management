from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment

class PaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ['customer', 'meter', 'meter_reading', 'amount']