"""
Serializers for medication SKU APIs
"""
from rest_framework import serializers

from core.models import MedicationSKU, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag object"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class MedicationSKUSerializer(serializers.ModelSerializer):
    """Serializer for MedicationSKU object"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = MedicationSKU
        fields = ['id', 'medication_name', 'presentation', 'dose',
                  'unit', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """
        overwriting the create method
        to allow creation of tags inside a medication sku
        """
        tags = validated_data.pop('tags', [])
        medication_sku = MedicationSKU.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # why not using name=tag['name']?
                # ** is future-proof in case we add more values to the Tag
                **tag,
            )
            medication_sku.tags.add(tag_obj)

        return medication_sku


class MedicationSKUDetailSerializer(MedicationSKUSerializer):
    """Serializer for MedicationSKU detail object"""

    class Meta(MedicationSKUSerializer.Meta):
        fields = MedicationSKUSerializer.Meta.fields
