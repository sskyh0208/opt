from django.db import models
from django.utils import timezone

# Create your models here.
class DevroomStatus(models.Model):
    temperature = models.DecimalField(max_digits=100, decimal_places=1)
    humidity = models.DecimalField(max_digits=100, decimal_places=1)
    co2 = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'devroom_status'