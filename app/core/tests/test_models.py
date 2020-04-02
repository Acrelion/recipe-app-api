from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with email is successful"""

        email = 'test@example.com'
        password = 'TestPass222'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if email domain is normalized"""

        email = 'test@HELLO.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='HelloKitty'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test if new user invalid email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'PassHello')