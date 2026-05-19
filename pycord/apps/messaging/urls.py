from __future__ import annotations

from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.app_home, name="home"),
    path("<slug:server_slug>/<slug:channel_slug>/", views.channel_view, name="channel"),
]
