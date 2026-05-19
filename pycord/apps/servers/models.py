"""Server / Channel / Membership domain — the spine of the Discord-style UX."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_puid.fields import PrefixedUIDField


class Server(models.Model):
    """A Discord-style 'guild' — a top-level container of channels."""

    puid = PrefixedUIDField(prefix="srv", random_length=10)
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)
    icon = models.ImageField(upload_to="servers/icons/", blank=True, null=True)
    banner = models.ImageField(upload_to="servers/banners/", blank=True, null=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="owned_servers",
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="Membership",
        related_name="servers",
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("servers:detail", args=[self.slug])


class Membership(models.Model):
    """Join table: user ↔ server, with role + nickname."""

    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("mod", "Moderator"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="member")
    nickname = models.CharField(max_length=64, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "server")]
        ordering = ["-joined_at"]

    def __str__(self) -> str:
        return f"{self.user} in {self.server} ({self.role})"


class Channel(models.Model):
    """A text channel within a server."""

    KIND_CHOICES = [
        ("text", "Text"),
        ("announcement", "Announcement"),
        ("voice", "Voice (placeholder)"),
    ]

    puid = PrefixedUIDField(prefix="chn", random_length=10)
    server = models.ForeignKey(
        Server, related_name="channels", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    kind = models.CharField(max_length=16, choices=KIND_CHOICES, default="text")
    topic = models.CharField(max_length=240, blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "name"]
        unique_together = [("server", "slug")]

    def __str__(self) -> str:
        return f"#{self.name}"

    @property
    def group_name(self) -> str:
        """Channel name on the WebSocket group bus."""
        return f"channel.{self.puid}"

    def get_absolute_url(self) -> str:
        return reverse("messaging:channel", args=[self.server.slug, self.slug])
