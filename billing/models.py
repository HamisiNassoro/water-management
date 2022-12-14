from django.db import models
from base import fields as custom_fields

from apps.meters.models import MeterManagement, UsageRate, UnitRate, MeterReading
from apps.profiles.models import Customer
class Billing(models.Model):
    meter = models.ForeignKey(MeterManagement,null=True,blank=True, on_delete=models.PROTECT)
    meter_reading = models.ForeignKey(MeterReading,null=True,blank=True, on_delete=models.PROTECT)
    unit_rate = models.ForeignKey(UnitRate,null=True,blank=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    is_paid = models.BooleanField(default='False')
    billing_date =models.DateTimeField(auto_now_add=True, blank=True, null=True)
    bill_code = custom_fields.SUBField(max_length=20, prefix='BILL-', null=True, blank=True)

    def __str__(self):
        return str(self.meter_reading)

    def save(self, *args, **kwargs):
        self.amount = (self.meter.meter_reading) * (self.unit_rate.units)
        super(Billing, self).save(*args, **kwargs)

    

class Payment(models.Model):
    payment_number =custom_fields.SUBField(
        max_length=20,
        prefix='PAY-',
        null=True,
        blank=True
    )

    customer = models.ForeignKey(
        Customer,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    meter = models.ForeignKey(
        MeterManagement,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    meter_reading = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    bill = models.ForeignKey(Billing,null=True,blank=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_number)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"