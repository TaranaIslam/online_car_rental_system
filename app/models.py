from django.db import models
from django.contrib.auth.models import User

class CarManager(models.Manager):
    def create_car(self, model, price_per_hour, image):
        car = self.model(model=model, price_per_hour=price_per_hour, image=image)
        car.save()
        return car

class Car(models.Model):
    model = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='car_images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_rented = models.BooleanField(default=False)
   
    objects = CarManager()

    def __str__(self):
        return self.model
   
class CartItem(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.car.model}"
