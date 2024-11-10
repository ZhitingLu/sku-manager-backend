"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import MedicationSKU
from medication_sku import serializers


class MedicationSKUViewSet(viewsets.ModelViewSet):
    """View for manage the medication sku APIs"""
    queryset = MedicationSKU.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return serializer class for request"""
        if self.action == 'list':
            # For listing all medication SKUs
            return serializers.MedicationSKUSerializer

        # For individual medication SKU details
        return serializers.MedicationSKUDetailSerializer

    def perform_create(self, serializer):
        """Create a new medication sku"""
        serializer.save(user=self.request.user)
