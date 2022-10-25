import logging

import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import MeterNotFound
from .models import MeterManagement
from .pagination import MeterManagementPagination
from .serializers import MeterManagementSerializer,MeterManagementCreateSerializer

# Create your views here.

logger = logging.getLogger(__name__)

class MeterManagementFilter(django_filters.FilterSet):
    meter_type = django_filters.CharFilter(
        field_name="meter_type", lookup_expr="iexact"
    )
    site_type = django_filters.CharFilter(
        field_name="site_type", lookup_expr="iexact"
    )

    class Meta:
        model = MeterManagement
        fields = ["meter_type", "site_type"]

class ListAllMetersAPIView(generics.ListAPIView):
    serializer_class = MeterManagementSerializer
    queryset = MeterManagement.objects.all().order_by("-created_at")
    pagination_class = MeterManagementPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = MeterManagementFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]


class ListCustomersMetersAPIView(generics.ListAPIView):
    
    serializer_class = MeterManagementSerializer
    pagination_class = MeterManagementPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = MeterManagementFilter
    search_fields = ["country", "city"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = MeterManagement.objects.filter(user=user).order_by(
            "-created_at"
        )  ### Getting all meters of a certain user/customer
        return queryset


#### Function based view of update
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_property_api_view(request, slug):
    try:
        meter = MeterManagement.objects.get(slug=slug)
    except MeterManagement.DoesNotExist:
        raise MeterNotFound

    user = request.user
    if meter.user != user:
        return Response(
            {"error": "You can't update or edit a Meter that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data
        serializer = MeterManagementSerializer(
            meter, data, many=False
        )  # updating one instance
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


### Function based view for creating Meter
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_meter_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.pkid
    serializer = MeterManagementCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"Meter {serializer.data.get('name')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


### Function based view for deleting
@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_property_api_view(request, slug):
    try:
        meter = MeterManagement.objects.get(slug=slug)
    except MeterManagement.DoesNotExist:
        raise MeterNotFound

    user = request.user
    if meter.user != user:
        return Response(
            {"error": "You can't delete a Meter that doesn't belong to you"},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = meter.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)


class MeterManagementSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MeterManagementCreateSerializer

    def post(self, request):
        queryset = MeterManagement.objects.filter(read_status=True)
        data = self.request.data

        meter_type = data["meter_type"]
        queryset = queryset.filter(meter_type__iexact=meter_type)

        site_type = data["site_type"]
        queryset = queryset.filter(site_type__iexact=site_type)

        catch_phrase = data["catch_phrase"]
        queryset = queryset.filter(description__icontains=catch_phrase)

        serializer = MeterManagementSerializer(queryset, many=True)

        return Response(serializer.data)
