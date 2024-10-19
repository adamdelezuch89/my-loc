"""
Serializers for river APIs
"""

from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from core.models import River


class RiverSerializer(GeoFeatureModelSerializer, serializers.ModelSerializer):
    """Serializer for rivers."""
    # TODO: Fix error about core.River.geometry in backend logs

    class Meta:
        model = River
        fields = ["id", "name", "type", "geometry", "description"]
        read_only_fields = ["id", "name", "type", "geometry", "description"]
        geo_field = "geometry"
