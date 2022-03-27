from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from product.models import Product
from django_extensions.db.models import *

# Create your models here.
class User(AbstractUser):
    choice = [('m', 'male'),
              ('f', 'female')]
    gender = models.CharField(max_length=6, choices=choice, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='avtar', null=True)
    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email


class UserAddress(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    address = models.CharField(max_length=90, null=True, blank=True)
    state = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    country = models.CharField(max_length=90)
    zipcode = models.CharField(max_length=9)

    def __str__(self):
        return self.address
class UserReview(TimeStampedModel, models.Model):
    user=models.ForeignKey(User,related_name="reviews",on_delete=models.CASCADE)
    rating = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    )
    summary = models.TextField()

class Wishlist(TimeStampedModel, models.Model):
    user=models.ForeignKey(User,related_name="wistlist",on_delete=models.CASCADE)
    products=models.ForeignKey(Product,related_name="product_wistlist",on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)
