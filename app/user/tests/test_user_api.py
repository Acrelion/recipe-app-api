from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload= {
            'email': 'first@user.com',
            'password': 'SomeStrongPass312',
            'name': 'Some Name'
        }
        res = self.client.post(payload, CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # get user, checking if created
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # never return password
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Creating a user that already exists"""
        payload = {
            'email': 'second@user.com',
            'password': 'SomeOtherPass333'
        }
        # init create user (so we already have it)
        create_user(**payload)
        # try to create user that exists
        res = self.client.post(payload, CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Password must be more than 5 characters"""
        payload = {
            'email': 'second@user.com',
            'password': 'pw'
        }
        res = self.client.post(payload, CREATE_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
