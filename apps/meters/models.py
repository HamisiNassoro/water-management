import random
import string
from django.utils import timezone
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel
from base import fields as custom_fields
from django.db import transaction

#from apps.profiles.models import *

User = get_user_model()

### Custom Model Manager
class MeterReadManager(models.Manager):
    def get_queryset(self):
        return (
            super(MeterReadManager, self)
            .get_queryset()
            .filter(read_status=True)
        )  #### The queryset will be called only if the read_status is true

class MeterTypes(models.Model):
    type_name = models.CharField(max_length=100, null=True, blank=True)
    type_code = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = "Meter Type"
        verbose_name_plural = "Meter Types"
class PricingCategory(models.Model):
    category_name = models.CharField(max_length=200, null=True, blank=True)
    category_rate = models.DecimalField(max_digits=8, decimal_places=4)
    category_number = models.CharField(max_length=200, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Pricing Category"
        verbose_name_plural = "Pricing Categories"
class Concentrator(models.Model):
    concentrator_name = models.CharField(max_length=200, null=True, blank=True)
    concentrator_number = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.concentrator_name

    class Meta:
        verbose_name = "Concentrator"
        verbose_name_plural = "Concentrators"
class MeterManagement(TimeStampedUUIDModel):
    class MeterType(models.TextChoices):
        MECHANICAL = "Mechanical", _("Mechanical")
        SMART = "Smart", _("Smart")

    class SiteType(models.TextChoices):
        BUILDING = "Building", _("Building")
        FARM = "Farm", _("Farm")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Site Manager,Meter Reader or Customer"),
        related_name="meter_owner",
        on_delete=models.DO_NOTHING,
    )
    #company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    meter_type = models.ForeignKey(MeterTypes,null=True,blank=True,on_delete=models.PROTECT)
    
    concentrator = models.ForeignKey(
        Concentrator,
        null=True,
        blank=True,
        on_delete=models.PROTECT
        )
    name = models.CharField(verbose_name=_("Site Name"), max_length=250)
    
    slug = AutoSlugField(
        populate_from="name", unique=True, always_update=True
    )  ### Means when name changes also update slug field
    ref_code = models.CharField(
        verbose_name=_("Meter Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    meter_code = custom_fields.SUBField(max_length=10, prefix='MET-', null=True, blank=True)
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description...update me please....",
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="KE",
        blank_label="(select country)",
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Nairobi")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="140"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="KG8 Avenue"
    )
    meter_number = models.IntegerField(
        verbose_name=_("Meter Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
  
    site_type = models.CharField(
        verbose_name=_("Site Type"),
        max_length=50,
        choices=SiteType.choices,
        default=SiteType.OTHER,
    )
    
    read_status = models.BooleanField(
        verbose_name=_("Reading Status"), default=False
    )

    initial_reading = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    current_reading = models.DecimalField(max_digits=12, decimal_places=4, default=0.0)
    objects = models.Manager()
    read = MeterReadManager()

    def __str__(self):
        return str(self.meter_code)

    class Meta:
        verbose_name = "Meter"
        verbose_name_plural = "Meters"

    def save(self, *args, **kwargs):
        self.name = str.title(self.name)  # name be title cased
        self.description = str.capitalize(
            self.description
        )  # description be capitalized
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(MeterManagement, self).save(*args, **kwargs)

    @property
    def final_meter_price(self):
        current_reading = self.current_reading
        initial_reading = self.initial_reading

class MeterMutationManager(models.Manager):
    @transaction.atomic
    def recalculate(self, from_:"MeterMutation"):
        qs = self.filter(
            meter = from_.meter, timestamp__gte=from_.timestamp, id__gt=from_.id
        ).select_for_update()

        prev = from_
        for mutation in qs:
            mutation.start_reading = prev.end_reading
            mutation.litre_usage = mutation.end_reading - mutation.start_reading
            mutation.save()
            prev = mutation
class MeterMutation(models.Model):
    id = models.BigAutoField(primary_key=True)
    meter = models.ForeignKey(
        MeterManagement,
        null=True, 
        blank=True,
        on_delete=models.CASCADE,
        related_name="mutations"
    )
    start_reading = models.DecimalField(decimal_places=4, max_digits=12, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    litre_usage = models.DecimalField(decimal_places=4, max_digits=12, null=True, blank=True)
    end_reading = models.DecimalField(decimal_places=4, max_digits=12, null=True, blank=True)
    

    objects = MeterMutationManager()

    class Meta:
        ordering = ('timestamp', 'pk')
class UsageRate(models.Model):
    eff_date = models.DateField(verbose_name='Effective Date')

    def __str__(self):
        return f'{self.eff_date}'

    class Meta:
        verbose_name = "Usage Rate"
        verbose_name_plural = "Usage Rates"

class UnitRate(models.Model):
    usage_rate = models.ForeignKey(UsageRate, on_delete=models.PROTECT)
    meter = models.ForeignKey(MeterManagement, on_delete=models.PROTECT)
    units = models.PositiveIntegerField()
    rate = models.DecimalField(
        verbose_name=_("Rate"), max_digits=8, decimal_places=2, default=0.0
    )
    def __str__(self):
        return f'{self.meter} {self.units}'

    class Meta:
        verbose_name = "Unit Rate"
        verbose_name_plural = "Unit Rates"

class MeterReading(models.Model):
    date = models.DateField(default=timezone.now)
    meter = models.ForeignKey(MeterManagement, on_delete=models.PROTECT)
    reader = models.ForeignKey(
        User,
        verbose_name=_("Meter Reader"),
        related_name="meter_read",
        on_delete=models.DO_NOTHING,
    )
    reading = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.meter} {self.date} {self.reader} {self.reading}'

    class Meta:
        verbose_name = "Meter Reading"
        verbose_name_plural = "Meter Readings"

    @property
    def previous_reading(self):
        reading = MeterReading.objects.filter(meter=self.meter,
                                              date__lt=self.date).values_list('reading', flat=True).order_by(
            '-date').first()
        return reading

    @property
    def usage(self):
        if self.previous_reading is None:
            return self.reading
        else:
            return self.reading - self.previous_reading

    @property
    def cost(self):
        usage_rate = UsageRate.objects.filter(eff_date__lte=self.date).order_by('-eff_date').first()
        unit_rates = UnitRate.objects.filter(usage_rate=usage_rate).values_list('units', 'rate').order_by(
            '-units')
        unit_rates = unit_rates[::1]
        usage = self.usage
        cost = 0
        for unit_rate in unit_rates:
            units = unit_rate[0]
            rate = unit_rate[1]
            if usage > units:
                used_units = usage - units
                used_units_price = used_units * rate
                cost += used_units_price
                usage = usage - used_units
        cost = round(cost, 2)
        return cost

    def __str__(self):
        return f'{self.date} {self.meter}'
