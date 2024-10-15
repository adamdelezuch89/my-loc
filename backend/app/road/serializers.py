"""
Serializers for road APIs
"""

from rest_framework import serializers

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from core.models import Road


class RoadSerializer(GeoFeatureModelSerializer, serializers.ModelSerializer):
    """Serializer for roads."""
    # TODO: Fix error about core.Road.geometry in backend logs

    class Meta:
        model = Road
        fields = ["id", "name", "type", "geometry", "description"]
        read_only_fields = ["id", "name", "type", "geometry", "description"]
        geo_field = "geometry"
