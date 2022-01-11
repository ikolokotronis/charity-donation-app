from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)


class Institution(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    type_choices = (
        (1, 'Fundacja'),
        (2, 'Organizacja pozarządowa'),
        (3, 'Zbiórka lokalna')
    )
    type = models.IntegerField(choices=type_choices, default=1)
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=100)
    pick_up_date = models.DateField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
