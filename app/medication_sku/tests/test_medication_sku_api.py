"""
Test for medication SKU API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MedicationSKU

from medication_sku.serializers import MedicationSKUSerializer

MEDICATION_SKU_LIST_URL = reverse('medication_sku:medication_sku-list')


def create_medication_sku(user, **params):
    """Create a new medication SKU"""
    defaults = {
        "medication_name": "Amoxicillin",
        "presentation": "Tablet",
        "dose": 50,
        "unit": "mg",
    }
    defaults.update(params)

    medication_sku = MedicationSKU.objects.create(user=user, **defaults)
    return medication_sku


class PublicMedicationSkuApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving medication skus"""
        res = self.client.get(MEDICATION_SKU_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMedicationSkuApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_medication_sku_list(self):
        """Test retrieving a list of medication skus"""
        create_medication_sku(user=self.user)
        create_medication_sku(user=self.user)

        res = self.client.get(MEDICATION_SKU_LIST_URL)

        medication_skus = MedicationSKU.objects.all().order_by('-id')
        serializer = MedicationSKUSerializer(medication_skus, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_medication_skus_limited_to_user(self):
        """Test retrieving medication skus only for the authenticated user"""
        other_user = get_user_model().objects.create_user(
            'otheruser@example.com',
            'testpass123',
        )
        create_medication_sku(user=other_user)
        create_medication_sku(user=self.user)

        res = self.client.get(MEDICATION_SKU_LIST_URL)

        medication_skus = MedicationSKU.objects.filter(user=self.user)
        serializer = MedicationSKUSerializer(medication_skus, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_duplicate_medication_name(self):
        """Test creating a new medication SKU with duplicate name fails"""
        create_medication_sku(user=self.user, medication_name="Ibuprofen")
        payload = {
            'medication_name': 'Ibuprofen',  # Duplicate medication_name
            'presentation': 'Tablet',
            'dose': 50,
            'unit': 'mg',
        }

        res = self.client.post(MEDICATION_SKU_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        #  "medication_name": [
        #       "This field must be unique."
        #   ]
        self.assertIn('medication_name', res.data)

    def test_create_duplicate_medication_presentation(self):
        """Test creating a new medication SKU with duplicate presentation fails"""
        create_medication_sku(
            user=self.user,
            medication_name="Ibuprofen",
            presentation="Tablet",
            dose=50,
            unit="mg",
        )
        payload = {
            "medication_name": "Ibuprofen",  # Duplicate combination
            "presentation": "Tablet",
            "dose": 50,
            "unit": "mg",
        }

        res = self.client.post(MEDICATION_SKU_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('medication_name', res.data)
