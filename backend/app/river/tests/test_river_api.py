"""
Tests for the river API.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import River

from river.serializers import RiverSerializer


RIVERS_URL = reverse("river:river-list")


def create_river(**params):
    """Create and return a sample river."""

    defaults = {
        "name": "Odra",
        "type": "river",
        "geometry": "LINESTRING(0 0, 1 1)",
        "description": "Sample river description.",
    }
    defaults.update(params)

    river = River.objects.create(**defaults)
    return river


class PRiverApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_non_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RIVERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_rivers(self):
        """Test retrieving a list of rivers."""
        create_river()
        create_river()

        res = self.client.get(RIVERS_URL)

        rivers = River.objects.all().order_by("-id")
        serializer = RiverSerializer(rivers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
