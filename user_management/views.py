from django.db.models.aggregates import Sum
from django.shortcuts import render
from rest_framework.decorators import *
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from rest_framework.status import *
from .models import *
from .serializers import *
from .tokens import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token


@api_view(['POST'])
def register_user(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        email_address = serializer.data['email_address']
        first_name = serializer.data['firstname']
        password = serializer.data['password']

        try:
            n = Customers.objects.get(email_address=email_address)
            return Response({'success': True, 'code': HTTP_401_UNAUTHORIZED, 'message': 'Customer already Exists'}, status=HTTP_401_UNAUTHORIZED)

        except ObjectDoesNotExist:
            User.objects.create_user(
                username=email_address, password=password, email=email_address)
            user = Customers(email_address=email_address,
                             firstname=first_name)
            user.save()
            token = account_activation_token.make_token(user)
            print(token)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('user_management/email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })
            to_email = email_address
            try:
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Customer registered successfully'}, status=HTTP_201_CREATED)
            except:

                return Response({'success': True, 'code': HTTP_401_UNAUTHORIZED, 'message': 'SMTP ERROR'}, status=HTTP_401_UNAUTHORIZED)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Customers._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Email Verified Successfully'}, status=HTTP_200_OK)

    else:
        return Response({'success': False, 'code': HTTP_401_UNAUTHORIZED, 'message': 'Email doesnt exist'}, status=HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email_address = serializer.data['email_address']
        password = serializer.data['password']
        try:
            user = authenticate(
                request, username=email_address, password=password)
            if user is not None:
                status = Customers.objects.get(
                    email_address=email_address).is_active
                if(status == True):
                    return Response({'Success': True, 'Code': 200, 'message': "Login Successful"}, status=HTTP_200_OK)
                else:
                    return Response({'Success': False, 'Code': HTTP_401_UNAUTHORIZED, 'message': 'account is not activated'}, status=HTTP_401_UNAUTHORIZED)

            else:
                return Response({'Success': False, 'Code': HTTP_401_UNAUTHORIZED, 'message': 'Details Dont Match'}, status=HTTP_401_UNAUTHORIZED)
        except:
            return Response({'Success': False, 'Code': HTTP_401_UNAUTHORIZED, 'message': 'Details Dont Match'}, status=HTTP_401_UNAUTHORIZED)
    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_update(request):
    serializer = UpdateSerializer(data=request.data)
    if serializer.is_valid():
        email_address = serializer.data.get('email_address')
        middlename = serializer.data.get('middlename')
        lastname = serializer.data.get('lastname')
        dob = serializer.data.get('dob')
        phone_number = serializer.data.get('phone_number')
        nationality = serializer.data.get('nationality')

        try:
            customer = Customers.objects.get(email_address=email_address)
            customer.middlename = middlename
            customer.lastname = lastname
            customer.dob = dob
            customer.phone_number = phone_number
            customer.nationality = nationality
            customer.save()
            return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Customer updated successfully'}, status=HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'success': False, 'code': HTTP_401_UNAUTHORIZED, 'message': 'Customer does not exist'}, status=HTTP_401_UNAUTHORIZED)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_address(request):
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        email_address = serializer.data['email_address']
        country = serializer.data['country']
        city = serializer.data['city']
        state = serializer.data['state']
        zip = serializer.data['zip']

        try:
            customer = Customers.objects.get(email_address=email_address)
            print(customer.id)
            try:
                address = Residential_address.objects.get(
                    customer_id=customer.id)
                address.country = country
                address.city = city
                address.state = state
                address.zip = zip
                address.save()
                return Response({'success': True, 'code': HTTP_200_OK, 'message': 'Address updated successfully'}, status=HTTP_200_OK)

            except:
                address = Residential_address(
                    country=country, city=city, state=state, zip=zip, email_address=email_address, customer_id=customer.id)
                address.save()

                return Response({'success': True, 'code': HTTP_201_CREATED, 'message': 'Address created successfully'}, status=HTTP_201_CREATED)

        except ObjectDoesNotExist:
            return Response({'success': True, 'code': HTTP_401_UNAUTHORIZED, 'message': 'Customer doesnt exist'}, status=HTTP_401_UNAUTHORIZED)

    return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)
