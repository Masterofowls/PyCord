"""Channels consumer for a single text channel.

Subscribers receive every `chat.message` group event broadcast by the
`Message.post_save` signal in `pycord.apps.messaging.signals`.

Inbound client events:
    {"action": "send", "content": "..."}
    {"action": "typing"}
"""

from __future__ import annotations

from typing import Any

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChannelConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self) -> None:
        self.user = self.scope.get("user")
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4401)
            return

        self.channel_puid: str = self.scope["url_route"]["kwargs"]["channel_puid"]
        channel = await self._load_channel(self.channel_puid, self.user.id)
        if channel is None:
            await self.close(code=4403)
            return

        self.channel_obj = channel
        self.group_name = f"channel.{self.channel_puid}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self.send_json({"event": "connected", "channel": self.channel_puid})

    async def disconnect(self, code: int) -> None:
        group = getattr(self, "group_name", None)
        if group:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def receive_json(self, content: dict[str, Any], **kwargs) -> None:
        action = content.get("action")
        if action == "send":
            text = (content.get("content") or "").strip()
            if not text:
                return
            await self._save_message(self.channel_obj.id, self.user.id, text)
            # signal handler will broadcast — no double-send here
        elif action == "typing":
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.typing",
                    "username": self.user.username,
                },
            )

    # --- group event handlers ----------------------------------------------
    async def chat_message(self, event: dict[str, Any]) -> None:
        await self.send_json({"event": event["event"], "message": event["message"]})

    async def chat_typing(self, event: dict[str, Any]) -> None:
        await self.send_json({"event": "typing", "username": event["username"]})

    # --- DB helpers --------------------------------------------------------
    @staticmethod
    @database_sync_to_async
    def _load_channel(channel_puid: str, user_id: int):
        from pycord.apps.servers.models import Channel

        return (
            Channel.objects.select_related("server")
            .filter(puid=channel_puid, server__members__id=user_id)
            .first()
        )

    @staticmethod
    @database_sync_to_async
    def _save_message(channel_id: int, author_id: int, content: str):
        from pycord.apps.messaging.models import Message

        return Message.objects.create(
            channel_id=channel_id,
            author_id=author_id,
            content=content,
        )
