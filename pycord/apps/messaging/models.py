"""Messages, reactions, attachments and direct-message threads."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django_puid.fields import PrefixedUIDField

from pycord.apps.servers.models import Channel


class Message(models.Model):
    puid = PrefixedUIDField(prefix="msg", random_length=10)
    channel = models.ForeignKey(
        Channel, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    reply_to = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="replies",
    )
    edited_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["channel", "-created_at"])]

    def __str__(self) -> str:
        return f"{self.author}: {self.content[:50]}"


class Reaction(models.Model):
    message = models.ForeignKey(
        Message, related_name="reactions", on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("message", "user", "emoji")]


class Attachment(models.Model):
    message = models.ForeignKey(
        Message, related_name="attachments", on_delete=models.CASCADE
    )
    file = models.FileField(upload_to="attachments/%Y/%m/")
    filename = models.CharField(max_length=200)
    content_type = models.CharField(max_length=80, blank=True)
    size = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class DirectMessageThread(models.Model):
    puid = PrefixedUIDField(prefix="dm", random_length=10)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="dm_threads"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def group_name(self) -> str:
        return f"dm.{self.puid}"


class DirectMessage(models.Model):
    thread = models.ForeignKey(
        DirectMessageThread, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
