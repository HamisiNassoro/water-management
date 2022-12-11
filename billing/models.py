from django.db import models
from base import fields as custom_fields

from apps.meters.models import MeterManagement, UsageRate, UnitRate, MeterReading

class Billing(models.Model):
    meter = models.ForeignKey(MeterManagement,null=True,blank=True, on_delete=models.PROTECT)
    meter_reading = models.ForeignKey(MeterReading,null=True,blank=True, on_delete=models.PROTECT)
    unit_rate = models.ForeignKey(UnitRate,null=True,blank=True, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2, editable=False)
    is_paid = models.BooleanField(default='False')
    billing_date =models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.meter_reading)

    def save(self, *args, **kwargs):
        self.amount = (self.meter.meter_reading) * (self.unit_rate.units)
        super(Billing, self).save(*args, **kwargs)

    

class Payment(models.Model):
    payment_id =custom_fields.SUBField(max_length=20, prefix='MET-', null=True, blank=True)
    bill = models.ForeignKey(Billing,null=True,blank=True, on_delete=models.PROTECT)
    
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)