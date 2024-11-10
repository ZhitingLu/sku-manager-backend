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
    serializer_class = serializers.MedicationSKUSerializer
    queryset = MedicationSKU.objects.all()
    # Require token authentication
    authentication_classes = [TokenAuthentication]
    # Only authenticated users can access
    permission_classes = [IsAuthenticated]
