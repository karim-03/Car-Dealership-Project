from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=(("Admin","Admin"),("Customer","Customer")), default="Customer")
    @property
    def name(self):
        return self.username


class Cars(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100)
    seller = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='available')

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year}) - {self.status}"

class Requests(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Cars, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Request {self.id} by {self.user_id} for {self.car_id}"