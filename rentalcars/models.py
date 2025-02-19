from django.db import models
from django.contrib.auth.models import User


# Model for Car
class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return str(self.name)

class Booking(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    rental_date = models.DateField()
    return_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_order_id = models.CharField(max_length=255, null=True, blank=True)  # Add this field
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return str(self.id)

