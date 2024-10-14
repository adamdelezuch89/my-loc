"""
Tests for models.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""

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

    def test_create_road(self):
        """Test creating a road is successful."""

        road = models.Road.objects.create(
            name="Main Street",
            type="street",
            geometry="LINESTRING(0 0, 1 1)",
            description="Sample road description.",
        )

        self.assertEqual(str(road), road.name)

    def test_create_road_unsupported_type_raises_error(self):
        """Test creating a road is successful."""

        with self.assertRaises(ValidationError):
            models.Road.objects.create(
                name="High Street",
                type="aaaa",
                geometry="LINESTRING(0 0, 1 1)",
                description="Sample road description.",
            )

    def test_create_road_incorrect_geometry_raises_error(self):
        """Test creating a road is successful."""

        with self.assertRaises(ValueError):
            models.Road.objects.create(
                name="Low Street",
                type="street",
                geometry="some wrong data",
                description="Sample road description.",
            )
