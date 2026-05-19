from __future__ import annotations

from rest_framework import serializers

from pycord.apps.servers.models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["puid", "name", "slug", "kind", "topic", "position", "server"]
        read_only_fields = ["puid"]


class ServerSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True, read_only=True)

    class Meta:
        model = Server
        fields = [
            "puid",
            "name",
            "slug",
            "description",
            "is_public",
            "channels",
            "created_at",
        ]
        read_only_fields = ["puid", "created_at"]
