from django.test import TestCase
from .models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

# Create your tests here.


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'email_address': 'juliuszakora@gmail.com',
                'firstname': 'julius', 'password': 'test1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customers.objects.count(), 1)
        self.assertEqual(Customers.objects.get().email_address,
                         'juliuszakora@gmail.com')

    def test_login(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('login')
        data = {'email_address': 'juliuszakora@gmail.com',
                'password': 'test1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_account_update(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('update')
        data = {'email_address': 'juliuszakora@gmail.com', 'middlename': 'test', 'lastname': 'test',
                'dob': 'test', 'nationality': 'test', 'phone_number': '25470000000'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_address_add(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('address')
        data = {'email_address': 'juliuszakora@gmail.com', 'country': 'Kenya', 'city': 'Nairobi',
                'state': 'Nairobi', 'zip': '10000'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
