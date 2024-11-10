"""
Views for the recipe APIs
"""
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import MedicationSKU
from medication_sku import serializers


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners to edit or delete their medication SKUs.
    All users can view, but only owners can modify.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the medication SKU
        return obj.user == request.user


class MedicationSKUViewSet(viewsets.ModelViewSet):
    """View for manage the medication sku APIs"""
    queryset = MedicationSKU.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

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

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        """Bulk create medication SKUs"""
        # Extract the list of medication SKUs from the request data
        data = request.data

        serializer = serializers.MedicationSKUSerializer(data=data, many=True)
        if serializer.is_valid():
            # Bulk create the medication SKUs
            medication_skus = []
            for item in serializer.validated_data:
                item['user'] = request.user  # Set the user to each SKU
                medication_skus.append(MedicationSKU(**item))

            MedicationSKU.objects.bulk_create(medication_skus)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
