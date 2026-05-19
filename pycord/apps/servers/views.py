from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Channel, Membership, Server
from .serializers import ChannelSerializer, ServerSerializer


class ServerViewSet(viewsets.ModelViewSet):
    serializer_class = ServerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return Server.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        server = serializer.save(owner=self.request.user)
        Membership.objects.create(user=self.request.user, server=server, role="owner")
        Channel.objects.create(
            server=server, name="general", slug="general", position=0
        )


class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "puid"

    def get_queryset(self):
        return Channel.objects.filter(server__members=self.request.user)


@login_required
@require_http_methods(["GET", "POST"])
def create_server(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        if name:
            slug = slugify(name)[:80] or "server"
            # ensure unique slug
            base, i = slug, 1
            while Server.objects.filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            server = Server.objects.create(name=name, slug=slug, owner=request.user)
            Membership.objects.create(user=request.user, server=server, role="owner")
            Channel.objects.create(
                server=server, name="general", slug="general", position=0
            )
            return redirect(
                "messaging:channel", server_slug=server.slug, channel_slug="general"
            )
    return render(request, "servers/create.html")


@login_required
def server_detail(request, slug: str):
    server = get_object_or_404(Server, slug=slug, members=request.user)
    first = server.channels.order_by("position").first()
    if first:
        return redirect(
            "messaging:channel", server_slug=server.slug, channel_slug=first.slug
        )
    return render(request, "servers/empty.html", {"server": server})
