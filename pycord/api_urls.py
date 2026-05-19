"""DRF API URL routes."""

from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from pycord.apps.messaging.views import MessageViewSet
from pycord.apps.servers.views import ChannelViewSet, ServerViewSet

router = DefaultRouter()
router.register("servers", ServerViewSet, basename="server")
router.register("channels", ChannelViewSet, basename="channel")
router.register("messages", MessageViewSet, basename="message")

urlpatterns = [path("v1/", include(router.urls))]
