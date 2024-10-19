"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.gis.db import models as gis_models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class River(gis_models.Model):
    """River object."""

    RIVER_TYPES = [
        ("lake", "Lake"),
        ("river", "River"),
    ]
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=RIVER_TYPES, default="river")
    geometry = gis_models.GeometryField()
    description = models.TextField(
        blank=True, help_text="A brief description of the river"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validation is called before saving
        super().save(*args, **kwargs)


class POIType(models.Model):
    """Point of Interest (POI) Type object."""

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class POIManager(models.Manager):
    def calculate_nearest_point(self, poi):
        # Ensure river geometry and coordinates are valid
        if poi.river.geometry and poi.coordinates:
            # Calculate the nearest point on the river geometry
            return poi.river.geometry.interpolate(
                poi.river.geometry.project(poi.coordinates)
            )
        raise ValueError(
            "River and coordinates must be defined to calculate \
            the nearest point on river."
        )


class POI(gis_models.Model):
    """Point Of Interest object."""

    name = models.CharField(max_length=255)
    type = models.ForeignKey(POIType, on_delete=models.CASCADE)
    coordinates = gis_models.PointField()
    river = models.ForeignKey(River, on_delete=models.CASCADE)
    nearest_point_on_river = gis_models.PointField(null=False)
    is_public = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    description = models.TextField(
        blank=True, help_text="A brief description of the point of interest"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Attach the custom manager
    objects = POIManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Use the manager to calculate the nearest point
        self.nearest_point_on_river = POI.objects.calculate_nearest_point(self)

        # Validate and save
        self.full_clean()
        super().save(*args, **kwargs)
