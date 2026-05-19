from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from pycord.apps.servers.models import Channel, Server

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """REST endpoint for messages. Realtime delivery happens via the WS consumer."""

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "puid"

    def get_queryset(self):
        qs = Message.objects.select_related("author", "channel").filter(
            channel__server__members=self.request.user,
            deleted=False,
        )
        channel = self.request.query_params.get("channel")
        if channel:
            qs = qs.filter(channel__puid=channel)
        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@login_required
def app_home(request):
    server = Server.objects.filter(members=request.user).order_by("name").first()
    if server:
        channel = server.channels.order_by("position").first()
        if channel:
            return redirect(
                "messaging:channel", server_slug=server.slug, channel_slug=channel.slug
            )
        return redirect("servers:detail", slug=server.slug)
    return render(request, "messaging/welcome.html")


@login_required
def channel_view(request, server_slug: str, channel_slug: str):
    server = get_object_or_404(Server, slug=server_slug, members=request.user)
    channel = get_object_or_404(Channel, server=server, slug=channel_slug)
    messages = (
        channel.messages.select_related("author")
        .filter(deleted=False)
        .order_by("-created_at")[:50]
    )
    return render(
        request,
        "messaging/channel.html",
        {
            "server": server,
            "channel": channel,
            "messages_qs": reversed(list(messages)),
        },
    )
