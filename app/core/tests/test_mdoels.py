"""
Test for models
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Creates and returns a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass555'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'test2@example.com'],
            ['TEST3@EXAMPLE.com', 'test3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """Test creating a new user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_medication_sku(self):
        """Test creating a new medication sku is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        medication_sku = models.MedicationSKU.objects.create(
            user=user,
            medication_name="Ibuprofen",
            presentation='Capsule',
            dose=50,
            unit='mg'
        )

        self.assertEqual(str(medication_sku), medication_sku.medication_name)

    def test_medication_name_unique(self):
        """Test that medication name must be unique"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        models.MedicationSKU.objects.create(
            user=user,
            medication_name="Ibuprofen",
            presentation='Capsule',
            dose=50,
            unit='mg',
        )

        with self.assertRaises(Exception):  # IntegrityError will be raised
            models.MedicationSKU.objects.create(
                user=user,
                medication_name="Ibuprofen",  # Duplicate name
                presentation='Tablet',
                dose=100,
                unit='mg',
            )

    def test_medication_sku_combination_unique(self):
        """Test that medication sku combination must be unique"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        models.MedicationSKU.objects.create(
            user=user,
            medication_name="Ibuprofen",
            presentation='Capsule',
            dose=50,
            unit='mg',
        )

        with self.assertRaises(Exception):  # IntegrityError will be raised
            models.MedicationSKU.objects.create(
                user=user,
                medication_name="Ibuprofen",  # Same name
                presentation='Capsule',  # Same presentation
                dose=50,  # Same dose
                unit='mg',  # Same unit
            )

    def test_create_tag(self):
        """Test creating a tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='New tag')

        self.assertEqual(str(tag), tag.name)
