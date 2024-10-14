"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.gis import admin as gis_admin

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)


class RoadAdmin(gis_admin.GISModelAdmin):
    # TODO: Parameters are not taken into consideration. fix it later
    # TODO: Fix js errors too
    default_lon = 21.0122  # Longitude for Warsaw
    default_lat = 52.2297  # Latitude for Warsaw
    default_zoom = 12  # Zoom level (adjust as needed)
    map_width = 800  # Width of the map in pixels
    map_height = 600  # Height of the map in pixels

    class Media:
        # Link your custom JavaScript for the map tiles
        js = ("core/js/custom_map.js",)


admin.site.register(models.Road, RoadAdmin)
