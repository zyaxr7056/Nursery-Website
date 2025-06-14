from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from unfold.admin import ModelAdmin

plant_choices = [
    ('Indoor', 'Indoor'),
    ('Outdoor', 'Outdoor'),
    ('Succulent', 'Succulent'),
    ('Cactus', 'Cactus'),
    ('Herb', 'Herb'),
    ('Flowering', 'Flowering'),
    ('Foliage', 'Foliage'),
    ('Tree', 'Tree'),
    ('Shrub', 'Shrub'),
    ('Vine', 'Vine')
]
class Plant(models.Model):
    name = models.CharField(max_length=100)
    Desciption = models.TextField()
    image = models.ImageField(upload_to='plants/', null=True, blank=True)
    Quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Category = models.CharField(choices=plant_choices)

    def __str__(self):
        return self.name
    
class User_details(AbstractBaseUser):
    user_name = models.CharField(max_length=100, unique=True)
    Phone_number = models.IntegerField()
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.user_name
    
