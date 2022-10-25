import random
import string
from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import TimeStampedUUIDModel


# Create your models here.

User = get_user_model()

### Custom Model Manager
class MeterReadManager(models.Manager):
    def get_queryset(self):
        return (
            super(MeterReadManager, self)
            .get_queryset()
            .filter(read_status=True)
        )  #### The queryset will be called only if the read_status is true

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
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
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
    meter_type = models.CharField(
        verbose_name=_("Meter Type"),
        max_length=50,
        choices=MeterType.choices,
        default=MeterType.MECHANICAL,
    )
    site_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=SiteType.choices,
        default=SiteType.OTHER,
    )
    initial_reading = models.IntegerField(verbose_name=_("Initial Meter Reading"), default=0)
    current_reading = models.IntegerField(verbose_name=_("Current Meter Reading"), default=0)
    read_status = models.BooleanField(
        verbose_name=_("Reading Status"), default=False
    )
    objects = models.Manager()
    read = MeterReadManager()

    def __str__(self):
        return self.name

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
