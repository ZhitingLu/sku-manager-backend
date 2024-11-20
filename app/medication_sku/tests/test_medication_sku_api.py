"""
Test for medication SKU API
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import (MedicationSKU,
                         Tag)
from medication_sku.serializers import (MedicationSKUSerializer,
                                        MedicationSKUDetailSerializer)

MEDICATION_SKU_LIST_URL = reverse('medication_sku:medication_skus-list')


def detail_url(medication_sku_id):
    """Create and return a medication SKU detail URL"""
    return reverse('medication_sku:medication_skus-detail',
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
        self.assertEqual(medication_sku.presentation,
                         payload['presentation']
                         )
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
        new_user = create_user(
            email='newuser@example.com',
            password='testpass123'
        )
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
        self.client.force_authenticate(user=self.user)

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

        res = self.client.post(
            '/api/medication_sku/medication_skus/bulk_create/',
            payload,
            format='json'
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(res.data), 2)


class MedicationSKUOwnershipTests(TestCase):
    """Test ownership permissions for medication SKU CRUD operations"""

    def setUp(self):
        """Set up the test environment"""
        self.client = APIClient()

        # Create two users using the create_user helper method
        self.user1 = create_user(
            email='user1unique@example.com',
            password='testpass123'
        )
        self.user2 = create_user(
            email='user2unique@example.com',
            password='testpass123'
        )

        # Clear previous medication SKUs if any for clean test state
        MedicationSKU.objects.filter(user=self.user1).delete()
        MedicationSKU.objects.filter(user=self.user2).delete()

        # Create a medication SKU for user1
        self.medication_sku1 = create_medication_sku(
            user=self.user1,
            medication_name="Ibuprofen original",
            presentation="Tablet",
            dose=50,
            unit="mg",
        )

        # Create a medication SKU for user2
        self.medication_sku2 = create_medication_sku(
            user=self.user2,
            medication_name="Paracetamol original",
            presentation="Tablet",
            dose=50,
            unit="mg",
        )

    def test_user_can_update_own_medication_sku(self):
        """Test that a user can update their own medication SKU"""
        self.client.force_authenticate(user=self.user1)
        payload = {'medication_name': 'Ibuprofen Updated'}
        url = detail_url(self.medication_sku1.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.medication_sku1.refresh_from_db()
        self.assertEqual(self.medication_sku1.medication_name,
                         'Ibuprofen Updated')

    def test_user_cannot_update_another_users_medication_sku(self):
        """Test that a user cannot update another user's medication SKU"""
        self.client.force_authenticate(user=self.user1)
        payload = {'medication_name': 'Paracetamol Updated'}
        url = detail_url(self.medication_sku2.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_medication_sku(self):
        """Test that a user can delete their own medication SKU"""
        self.client.force_authenticate(user=self.user1)
        url = detail_url(self.medication_sku1.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure the SKU no longer exists
        self.assertFalse(
            MedicationSKU.objects.filter(id=self.medication_sku1.id).exists()
        )

    def test_user_cannot_delete_another_users_medication_sku(self):
        """Test that a user cannot delete another user's medication SKU"""
        self.client.force_authenticate(user=self.user1)
        url = detail_url(self.medication_sku2.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_medication_sku_new_tags(self):
        """Test creating a new medication SKU with new tags"""
        self.client.force_authenticate(user=self.user1)
        # Clear previous medication SKUs if any for clean test state
        MedicationSKU.objects.filter(user=self.user1).delete()

        payload = {
            'medication_name': 'Some medication name 1',
            'presentation': 'Tablet',
            'dose': 50,
            'unit': 'mg',
            'tags': [
                {'name': 'Anti-inflammatory',
                 },
                {'name': 'Antidepressant',
                 }
            ]
        }
        res = self.client.post(MEDICATION_SKU_LIST_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        medication_skus = MedicationSKU.objects.filter(user=self.user1)

        self.assertEqual(medication_skus.count(), 1)
        medication_sku = medication_skus.first()
        self.assertEqual(medication_sku.tags.count(), 2)
        for tag in payload['tags']:
            exists = medication_sku.tags.filter(
                name=tag['name'],
                user=self.user1,
            ).exists()
            self.assertTrue(exists)

    def test_create_medication_sku_with_existing_tags(self):
        """Test creating a new medication SKU with existing tags"""
        self.client.force_authenticate(user=self.user1)
        # Clear previous medication SKUs if any for clean test state
        MedicationSKU.objects.filter(user=self.user1).delete()

        tag_anesthetic = Tag.objects.create(user=self.user1, name='Anesthetic')
        payload = {
            'medication_name': 'Some medication name 2',
            'presentation': 'Tablet',
            'dose': 50,
            'unit': 'mg',
            'tags': [{
                'name': 'Anti-inflammatory',
            },
                {'name': 'Anesthetic', }]
        }
        res = self.client.post(MEDICATION_SKU_LIST_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        medication_skus = MedicationSKU.objects.filter(user=self.user1)
        self.assertEqual(medication_skus.count(), 1)
        medication_sku = medication_skus.first()
        self.assertEqual(medication_sku.tags.count(), 2)
        # test the existing tag is assigned to the medication_sku
        # instead of creating a duplicated tag
        self.assertIn(tag_anesthetic, medication_sku.tags.all())
        for tag in payload['tags']:
            exists = medication_sku.tags.filter(
                name=tag['name'],
                user=self.user1,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test creating a new tag when updating a medication SKU"""
        self.client.force_authenticate(user=self.user1)
        medication_sku = create_medication_sku(user=self.user1)
        payload = {
            'tags': [
                {'name': 'Sleep Aid'}
            ]
        }
        url = detail_url(medication_sku.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user1, name='Sleep Aid')
        self.assertIn(new_tag, medication_sku.tags.all())

    def test_update_medication_sku_assign_tag(self):
        """Test assigning an existing tag when updating a medication SKU"""
        self.client.force_authenticate(user=self.user1)
        # create a new tag
        # create a new medication_sku
        # add the crated tag to the created medication sku
        tag_vaccine = Tag.objects.create(user=self.user1, name='Vaccine')
        medication_sku = create_medication_sku(user=self.user1)
        medication_sku.tags.add(tag_vaccine)

        # create another tag
        # change the 'Vaccine' tag to 'Sedative' through the payload
        # send a HTTP PATCH with the payload
        tag_sedative = Tag.objects.create(user=self.user1, name='Sedative')
        payload = {
            'tags': [{
                'name': 'Sedative',
            }]
        }
        url = detail_url(medication_sku.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_sedative, medication_sku.tags.all())
        self.assertNotIn(tag_vaccine, medication_sku.tags.all())


def test_clear_medication_sku_tags(self):
    """Test clearing medication SKU tags"""
    self.client.force_authenticate(user=self.user1)
    tag = Tag.objects.create(user=self.user1, name='Anesthetic')
    medication_sku = create_medication_sku(user=self.user1)
    medication_sku.tags.add(tag)

    payload = {
        'tags': []
    }
    url = detail_url(medication_sku.id)
    res = self.client.patch(url, payload, format='json')

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(medication_sku.tags.count(), 0)
