"""
Test for medication SKU API
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MedicationSKU
from medication_sku.serializers import (MedicationSKUSerializer,
                                        MedicationSKUDetailSerializer)

MEDICATION_SKU_LIST_URL = reverse('medication_sku:medication_sku-list')


def detail_url(medication_sku_id):
    """Create and return a medication SKU detail URL"""
    return reverse('medication_sku:medication_sku-detail',
                   args=[medication_sku_id]
                   )


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


def create_user(**params):
    """Create a new user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com',
                                password='testpass123',
                                )
        self.client.force_authenticate(self.user)

    def test_retrieve_medication_sku_list(self):
        """Test retrieving a list of medication skus"""
        create_medication_sku(
            user=self.user,
            medication_name="Ibuprofen",
            presentation="Tablet",
            dose=50,
            unit="mg",
        )
        create_medication_sku(
            user=self.user,
            medication_name="Paracetamol",
            presentation="Tablet",
            dose=50,
            unit="mg",
        )

        res = self.client.get(MEDICATION_SKU_LIST_URL)

        medication_skus = MedicationSKU.objects.all().order_by('-id')
        serializer = MedicationSKUSerializer(medication_skus, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertCountEqual(res.data, serializer.data)

    def test_create_medication_sku(self):
        """Test creating a new medication SKU"""
        payload = {
            'medication_name': 'Aspirin',
            'presentation': 'Tablet',
            'dose': 50,
            'unit': 'mg',
        }
        res = self.client.post(MEDICATION_SKU_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        medication_sku = MedicationSKU.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(medication_sku, k), v)
        self.assertEqual(medication_sku.user, self.user)

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

    def test_create_duplicate_medication_combination(self):
        """
        Test creating a new medication SKU with duplicate combination fails
        """
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

    def test_retrieve_medication_sku_detail(self):
        """Test retrieving a medication SKU detail"""
        medication_sku = create_medication_sku(user=self.user)

        url = detail_url(medication_sku.id)
        res = self.client.get(url)

        serializer = MedicationSKUDetailSerializer(medication_sku)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test updating a medication SKU"""
        original_medication_name = 'Original name'
        original_dose = 50
        original_unit = 'mg'
        medication_sku = create_medication_sku(
            user=self.user,
            medication_name=original_medication_name,
            presentation='Original presentation',
            dose=original_dose,
            unit=original_unit,
        )

        payload = {
            'presentation': 'New presentation',
        }
        url = detail_url(medication_sku.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        medication_sku.refresh_from_db()
        self.assertEqual(medication_sku.user, self.user)
        self.assertEqual(medication_sku.medication_name,
                         original_medication_name)
        self.assertEqual(medication_sku.presentation, payload['presentation'])
        self.assertEqual(medication_sku.dose, original_dose)
        self.assertEqual(medication_sku.unit, original_unit)


def test_full_update(self):
    """Test fully updating a medication SKU"""
    medication_sku = create_medication_sku(
        user=self.user,
        medication_name="Sample name",
        presentation="Tablet",
        dose=50,
        unit="mg",
    )

    payload = {
        'medication_name': 'New name',
        'presentation': 'New presentation',
        'dose': 100,
        'unit': 'mg',
    }
    url = detail_url(medication_sku.id)
    res = self.client.put(url, payload)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    medication_sku.refresh_from_db()
    for k, v in payload.items():
        self.assertEqual(getattr(medication_sku, k), v)
    self.assertEqual(medication_sku.user, self.user)


def test_update_user_returns_error(self):
    """Test updating a medication SKU's user returns error"""
    new_user = create_user(email='user@example.com', password='testpass123')
    medication_sku = create_medication_sku(user=self.user)

    payload = {
        'user': new_user.id,
    }

    url = detail_url(medication_sku.id)
    self.client.put(url, payload)

    medication_sku.refresh_from_db()
    self.assertEqual(medication_sku.user, self.user)


def test_delete_medication_sku(self):
    """Test deleting a medication SKU successfully"""
    medication_sku = create_medication_sku(user=self.user)

    url = detail_url(medication_sku.id)
    res = self.client.delete(url)

    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    self.assertFalse(MedicationSKU.objects.filter(
        id=medication_sku.id
    ).exists())


def test_bulk_create_medication_skus(self):
    """Test bulk creating medication SKUs"""
    payload = [
        {
            'medication_name': 'Unique Aspirin',
            'presentation': 'Tablet',
            'dose': 50,
            'unit': 'mg'
        },
        {
            'medication_name': 'Unique Amoxicillin',
            'presentation': 'Capsule',
            'dose': 500,
            'unit': 'mg'
        }
    ]

    res = self.client.post('/medication_skus/bulk_create/', payload)

    self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    self.assertEqual(len(res.data), 2)

    # Check that both SKUs were created
    for item in payload:
        self.assertTrue(MedicationSKU.objects.filter(
            medication_name=item['medication_name'],
            presentation=item['presentation'],
            dose=item['dose'],
            unit=item['unit'],
            user=self.user
        ).exists())
