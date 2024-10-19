"""
URL mappings for the river app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from river import views


router = DefaultRouter()
router.register("rivers", views.RiverViewSet)

app_name = "river"

urlpatterns = [
    path("", include(router.urls)),
]
