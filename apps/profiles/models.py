from email.policy import default
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import TimeStampedUUIDModel
from apps.meters.models import  MeterManagement
from base import fields as custom_fields
User = get_user_model()


class Gender(models.TextChoices):
    MALE = "Male", _("Male")
    FEMALE = "Female", _("Female")
    OTHER = "Other", _("Other")


class Profile(TimeStampedUUIDModel):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+254712345678"
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("Country"), default="KE", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Nairobi",
        blank=False,
        null=False,
    )
    site_manager = models.BooleanField(verbose_name = _("Site Manager"), default=False,help_text=_("Are you a Site Manager?"),)
    meter_reader = models.BooleanField(verbose_name = _("Meter Reader"), default=False,help_text=_("Are you a Meter Reader?"),)
    is_cutomer = models.BooleanField(verbose_name= _("Customer"), default=False,help_text=_("Are you a Customer?"),)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Company(models.Model):
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_number = models.CharField(max_length=200, null=True, blank=True)
    company_description = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

class District(models.Model):
    district_name = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    district_description = models.CharField(max_length=200, null=True, blank=True)
    district_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.district_name

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
class SalesStation(models.Model):
    station_name = models.CharField(max_length=200, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    station_number = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.station_name

    class Meta:
        verbose_name = "Sales Station"
        verbose_name_plural = "Sales Stations"
class Customer(models.Model):
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    customer_number = custom_fields.SUBField(max_length=20, prefix="CUST-", null=True, blank=True)
    
    account_id= models.CharField(max_length=200, null=True, blank=True)
    customer_address = models.CharField(max_length=200, null=True, blank=True)
    customer_phone = models.CharField(max_length=200, null=True, blank=True)
    customer_email = models.CharField(max_length=200, null=True, blank=True)
    price_categories = models.CharField(max_length=200, null=True, blank=True)
    meter = models.ForeignKey(MeterManagement, null=True, blank=True, on_delete=models.PROTECT)
    meter_type = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.customer_number

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


