"""Broadcast new messages to the channel group on save."""

from __future__ import annotations

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message
from .serializers import MessageSerializer


@receiver(post_save, sender=Message)
def broadcast_message(sender, instance: Message, created: bool, **kwargs) -> None:
    layer = get_channel_layer()
    if layer is None:
        return
    payload = MessageSerializer(instance).data
    async_to_sync(layer.group_send)(
        instance.channel.group_name,
        {
            "type": "chat.message",
            "event": "message.created" if created else "message.updated",
            "message": payload,
        },
    )
