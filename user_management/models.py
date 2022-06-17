from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.


class Customers(models.Model):
    email_address = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    middlename = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    dob = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    last_login = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # history = HistoricalRecords()

    def __str__(self):
        return self.email_address


class Residential_address(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # history = HistoricalRecords()
