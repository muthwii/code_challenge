from django.db.models import fields
from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('email_address', 'firstname', 'password')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('email_address', 'password')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ('email_address', 'middlename', 'lastname',
                  'dob', 'nationality', 'phone_number')


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Residential_address
        fields = ('country', 'city', 'state',
                  'zip', 'email_address')
