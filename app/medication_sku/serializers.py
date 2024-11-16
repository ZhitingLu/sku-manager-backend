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

    def _get_or_create_tags(self, tags, medication_sku):
        """Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                # why not using name=tag['name']?
                # ** is future-proof in case we add more values to the Tag
                **tag,
            )
            medication_sku.tags.add(tag_obj)

    def create(self, validated_data):
        """
        Create a new medication SKU
        & allow creation of tags inside a medication sku
        """
        tags = validated_data.pop('tags', [])
        medication_sku = MedicationSKU.objects.create(**validated_data)
        self._get_or_create_tags(tags, medication_sku)

        return medication_sku

    def update(self, instance, validated_data):
        """
        Update a medication SKU
        & allow updating of tags inside a medication sku
        """
        tags = validated_data.pop('tags', None)
        if tags is not None:
            # we clear tags
            # if 'tags' is empty [], there won't be any tags
            # if not empty, we call the _get_or_create_tags
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        # everything outside the tags value
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class MedicationSKUDetailSerializer(MedicationSKUSerializer):
    """Serializer for MedicationSKU detail object"""

    class Meta(MedicationSKUSerializer.Meta):
        fields = MedicationSKUSerializer.Meta.fields
