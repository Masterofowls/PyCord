"""User account model — Discord-style profile fields layered onto AbstractUser."""

from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_puid.fields import PrefixedUIDField


class User(AbstractUser):
    """Application user.

    `puid` is a public, URL-safe short identifier (Discord-like handle).
    """

    puid = PrefixedUIDField(prefix="usr", random_length=10)
    display_name = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    status = models.CharField(
        max_length=16,
        choices=[
            ("online", "Online"),
            ("idle", "Idle"),
            ("dnd", "Do not disturb"),
            ("offline", "Offline"),
        ],
        default="online",
    )
    bio = models.TextField(blank=True)
    accent_color = models.CharField(max_length=7, default="#5865F2")

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return self.display_name or self.username

    @property
    def handle(self) -> str:
        return f"@{self.username}"
