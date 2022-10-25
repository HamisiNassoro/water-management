from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from .models import MeterManagement


class MeterManagementSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    country = CountryField(name_only=True)


    class Meta:
        model = MeterManagement
        fields = [
            "id",
            "user",
            "name",
            "slug",
            "ref_code",
            "description",
            "country",
            "city",
            "postal_code",
            "street_address",
            "meter_number",
            "site_type",
            "initial_reading",
            "current_reading",
            "read_status",
        ]

    def get_user(self, obj):
        return obj.user.username


class MeterManagementCreateSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = MeterManagement
        exclude = ["updated_at", "pkid"]