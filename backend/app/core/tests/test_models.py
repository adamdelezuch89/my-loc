"""
Tests for models.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point, LineString
from django.contrib.auth import get_user_model
from core import models


class UserModelTests(TestCase):
    """Test user model."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class RiverModelTests(TestCase):
    def test_create_river(self):
        """Test creating a river is successful."""

        river = models.River.objects.create(
            name="Main River",
            type="river",
            geometry="LINESTRING(0 0, 1 1)",
            description="Sample river description.",
        )

        self.assertEqual(str(river), river.name)

    def test_create_river_unsupported_type_raises_error(self):
        """Test creating a river is successful."""

        with self.assertRaises(ValidationError):
            models.River.objects.create(
                name="High River",
                type="aaaa",
                geometry="LINESTRING(0 0, 1 1)",
                description="Sample river description.",
            )

    def test_create_river_incorrect_geometry_raises_error(self):
        """Test creating a river is successful."""

        with self.assertRaises(ValueError):
            models.River.objects.create(
                name="Low River",
                type="river",
                geometry="some wrong data",
                description="Sample river description.",
            )


class POITypeTests(TestCase):
    def setUp(self):
        """Set up a basic POIType object."""
        models.POIType.objects.create(name="Restaurant")

    def test_poi_type_creation(self):
        """Test if a POIType object can be successfully created."""
        poi_type = models.POIType.objects.get(name="Restaurant")
        self.assertEqual(poi_type.name, "Restaurant")

    def test_poi_type_string_representation(self):
        """Test the string representation of POIType object."""
        poi_type = models.POIType.objects.get(name="Restaurant")
        self.assertEqual(str(poi_type), "Restaurant")

    def test_unique_name_constraint(self):
        """Test that POIType name field must be unique."""
        with self.assertRaises(Exception):
            models.POIType.objects.create(name="Restaurant")


class POITests(TestCase):
    def setUp(self):
        """Set up a user, a river, and a POIType for testing."""
        self.user = models.User.objects.create_user(
            email="test@example.com",
            password="testpass123",
        )
        self.river = models.River.objects.create(
            name="Maine",
            type="river",
            geometry=LineString(Point(0, 0), Point(2, 2)),
        )
        self.poi_type = models.POIType.objects.create(name="Restaurant")

    def test_poi_creation(self):
        """Test if a POI object can be successfully created."""
        poi = models.POI.objects.create(
            name="Pizza Place",
            type=self.poi_type,
            coordinates=Point(1, 1),
            river=self.river,
            author=self.user,
        )
        self.assertEqual(poi.name, "Pizza Place")

    def test_missing_coordinates(self):
        """Test that creating a POI without coordinates raises a ValidationError."""
        with self.assertRaises(ValueError):
            models.POI.objects.create(
                name="Missing Coordinates",
                type=self.poi_type,
                river=self.river,
                author=self.user,
            )

    def test_missing_river(self):
        """Test that creating a POI without a river raises a ValidationError."""
        with self.assertRaises(models.POI.river.RelatedObjectDoesNotExist):
            models.POI.objects.create(
                name="Missing River",
                type=self.poi_type,
                coordinates=Point(1, 1),
                author=self.user,
            )

    def test_invalid_coordinates(self):
        """Test that creating a POI with invalid coordinates
        raises a ValidationError."""
        with self.assertRaises(ValueError):
            models.POI.objects.create(
                name="Invalid POI",
                type=self.poi_type,
                coordinates="INVALID COORDINATES",  # Invalid type
                river=self.river,
                author=self.user,
            )

    def test_nearest_point_calculation(self):
        """Test that nearest_point_on_river is correctly calculated."""
        poi = models.POI.objects.create(
            name="Pizza Place",
            type=self.poi_type,
            coordinates=Point(1, 1),
            river=self.river,
            author=self.user,
        )
        nearest_point = poi.nearest_point_on_river
        expected_nearest_point = self.river.geometry.interpolate(
            self.river.geometry.project(poi.coordinates)
        )
        self.assertEqual(nearest_point.x, expected_nearest_point.x)
        self.assertEqual(nearest_point.y, expected_nearest_point.y)
