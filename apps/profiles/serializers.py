from django_countries.serializer_fields import CountryField
from rest_framework import fields, serializers

from .models import Profile,Customer


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    is_staff = serializers.BooleanField(source="user.is_staff")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "id",
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "site_manager",
            "meter_reader",
            "is_cutomer",
            "is_staff",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "site_manager",
            "meter_reader",
            "is_cutomer",
        ]

###################################################################
########################NEW RELATIONAL SERIALIZERS#################
###################################################################
class CustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = [
            'user',
            'company',
            'meter_type',
            'account_id',
            'customer_address',
            'customer_phone',
            'customer_email',
            'meter'
        ]
