from __future__ import annotations

from django.urls import path

from . import views

app_name = "servers"

urlpatterns = [
    path("new/", views.create_server, name="create"),
    path("<slug:slug>/", views.server_detail, name="detail"),
]
