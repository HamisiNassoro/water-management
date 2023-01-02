from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from .serializers import PaymentSerializer
from .models import Payment

from django_filters.rest_framework import DjangoFilterBackend
from .filters import PaymentFilter


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        payment = get_object_or_404(PaymentSerializer, pk=pk)

        if payment.orderitems.count() > 0:
            return Response({'error': 'Payment cannot be deleted'})
        payment.delete()