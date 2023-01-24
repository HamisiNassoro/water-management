from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import NotYourProfile, ProfileNotFound
from .models import Profile,Customer
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, UpdateProfileSerializer,CustomerSerializer

from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CustomerFilter
from rest_framework.filters import SearchFilter
from .permissions import IsAdminOrReadOnly

class SiteManagersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(site_manager=True)
    serializer_class = ProfileSerializer


"""
    from rest_framework import api_view, permissions

    @api_view(["GET"])
    @permission_classes((permissions.IsAuthenticated))
    def get_all_site_managers(request):
        site_managers = Profile.objects.filter(is_agent=True)
        serializer=ProfileSerializer(site_managers, many=True)
        name_spaced_response={"site_managers": serializer.data}
        return Response(name_spaced_response,status=status.HTTP_200_OK)
"""

class MeterReadersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(meter_reader=True)
    serializer_class = ProfileSerializer

class CustomersListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_cutomer=True)
    serializer_class = ProfileSerializer

class GetProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    def get(self, request):
        user = self.request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [ProfileJSONRenderer]

    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            raise ProfileNotFound

        user_name = request.user.username
        super_user = request.user.is_superuser
        if not super_user and  user_name != username:
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = CustomerFilter
    search_fields = ['customer_name', 'customer_number']
    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        customer = get_object_or_404(CustomerSerializer, pk=pk)

        if customer.orderitems.count() > 0:
            return Response({'error': 'Customer cannot be deleted'})
        customer.delete()