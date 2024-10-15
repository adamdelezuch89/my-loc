"""
Tests for the road API.
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Road

from road.serializers import RoadSerializer


ROADS_URL = reverse("road:road-list")


def create_road(**params):
    """Create and return a sample road."""

    defaults = {
        "name": "Main Street",
        "type": "street",
        "geometry": "LINESTRING(0 0, 1 1)",
        "description": "Sample road description.",
    }
    defaults.update(params)

    road = Road.objects.create(**defaults)
    return road


class PRoadApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_non_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ROADS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_roads(self):
        """Test retrieving a list of roads."""
        create_road()
        create_road()

        res = self.client.get(ROADS_URL)

        roads = Road.objects.all().order_by("-id")
        serializer = RoadSerializer(roads, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
