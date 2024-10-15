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


class RoadAdmin(gis_admin.GISModelAdmin):
    # TODO: Parameters are not taken into consideration. fix it later
    # TODO: Fix js errors too
    # TODO: Make sure, if geometry changes, reacalculate all
    # related objects - points, other roads

    default_lon = 21.0122  # Longitude for Warsaw
    default_lat = 52.2297  # Latitude for Warsaw
    default_zoom = 12  # Zoom level (adjust as needed)
    map_width = 800  # Width of the map in pixels
    map_height = 600  # Height of the map in pixels

    ordering = ["name"]
    search_fields = ["name"]

    list_filter = ["type"]  # Add filters for these fields

    class Media:
        # Link your custom JavaScript for the map tiles
        js = ("core/js/custom_map.js",)


class POITypeAdmin(admin.ModelAdmin):
    """Admin interface for POIType."""

    list_display = ["name"]
    search_fields = ["name"]


class POIAdmin(gis_admin.GISModelAdmin, admin.ModelAdmin):
    """Admin interface for POI."""

    # GIS map parameters for the POI admin interface
    default_lon = 21.0122  # Longitude for Warsaw
    default_lat = 52.2297  # Latitude for Warsaw
    default_zoom = 12  # Zoom level (adjust as needed)
    map_width = 800  # Width of the map in pixels
    map_height = 600  # Height of the map in pixels

    # TODO: Add waiting for approve window
    # TODO: Add coordinates display
    # TODO: Make sure, if coordinates changed, nearest point will be changed too
    list_display = [
        "name",
        "type",
        "road",
        "author",
        "is_public",
        "is_approved",
    ]
    list_filter = [
        "type",
        "is_public",
        "is_approved",
        "author",
        "road",
    ]

    search_fields = ["name"]
    readonly_fields = ["nearest_point_on_road"]

    # Default values for fields that should not require input
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Set default values for is_public and is_approved
        if obj is None:  # Only apply for new objects
            form.base_fields["is_public"].initial = True
            form.base_fields["is_approved"].initial = True
            form.base_fields["author"].initial = request.user
        return form

    def save_model(self, request, obj, form, change):
        """Override save_model to handle nearest point recalculation."""
        # If coordinates or road have changed, recalculate nearest_point_on_road
        if "coordinates" in form.changed_data or "road" in form.changed_data:
            obj.nearest_point_on_road = models.POI.objects.calculate_nearest_point(obj)

        # Call the superclass method to save the object
        super().save_model(request, obj, form, change)

    class Media:
        # Link your custom JavaScript for the map tiles
        js = ("core/js/custom_map.js",)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.POI, POIAdmin)
admin.site.register(models.POIType, POITypeAdmin)
admin.site.register(models.Road, RoadAdmin)
