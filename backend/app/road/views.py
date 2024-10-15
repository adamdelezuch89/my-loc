"""
Views for the road APIs
"""

from rest_framework import viewsets
# Create your views here.
from core.models import Road
from road import serializers


class RoadViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage road APIs."""

    serializer_class = serializers.RoadSerializer
    queryset = Road.objects.all()

    def get_queryset(self):
        """Retrieve roads for authenticated user."""
        # TODO: Replace with filtering by geolocation or ids-group
        return self.queryset.order_by("-id")
