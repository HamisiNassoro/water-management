from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment


class MeterViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        payment = get_object_or_404(PaymentSerializer, pk=pk)

        if payment.orderitems.count() > 0:
            return Response({'error': 'Payment cannot be deleted'})
        payment.delete()