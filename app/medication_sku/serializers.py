"""
Serializers for medication SKU APIs
"""
from rest_framework import serializers

from core.models import MedicationSKU, Tag


class MedicationSKUSerializer(serializers.ModelSerializer):
    """Serializer for MedicationSKU object"""

    class Meta:
        model = MedicationSKU
        fields = ['id', 'medication_name', 'presentation', 'dose', 'unit']
        read_only_fields = ['id']


class MedicationSKUDetailSerializer(MedicationSKUSerializer):
    """Serializer for MedicationSKU detail object"""

    class Meta(MedicationSKUSerializer.Meta):
        fields = MedicationSKUSerializer.Meta.fields


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag object"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
