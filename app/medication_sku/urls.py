"""
URL mappings for the medication sku app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from medication_sku import views as medication_sku_views

router = DefaultRouter()
router.register('medication_skus', medication_sku_views.MedicationSKUViewSet,
                basename='medication_skus')
router.register('tags', medication_sku_views.TagViewSet)

app_name = 'medication_sku'

urlpatterns = [
    path('', include(router.urls)),
]
