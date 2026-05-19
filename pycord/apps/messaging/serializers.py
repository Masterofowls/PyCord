from __future__ import annotations

from rest_framework import serializers

from .models import Attachment, Message, Reaction


class AttachmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = ["id", "url", "filename", "content_type", "size"]

    def get_url(self, obj: Attachment) -> str:
        return obj.file.url


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["emoji", "user"]


class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_display = serializers.CharField(source="author.display_name", read_only=True)
    author_avatar = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True, read_only=True)
    reactions = ReactionSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = [
            "puid",
            "channel",
            "content",
            "reply_to",
            "author_username",
            "author_display",
            "author_avatar",
            "attachments",
            "reactions",
            "edited_at",
            "created_at",
            "deleted",
        ]
        read_only_fields = ["puid", "created_at", "edited_at", "deleted"]

    def get_author_avatar(self, obj: Message) -> str | None:
        if obj.author.avatar:
            return obj.author.avatar.url
        return None
