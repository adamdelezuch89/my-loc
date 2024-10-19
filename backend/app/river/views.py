"""
Views for the river APIs
"""

from rest_framework import viewsets
# Create your views here.
from core.models import River
from river import serializers


class RiverViewSet(viewsets.ReadOnlyModelViewSet):
    """View for manage river APIs."""

    serializer_class = serializers.RiverSerializer
    queryset = River.objects.all()

    def get_queryset(self):
        """Retrieve rivers for authenticated user."""
        # TODO: Replace with filtering by geolocation or ids-group
        return self.queryset.order_by("-id")
