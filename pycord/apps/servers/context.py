"""Template context — sidebar of servers for the logged-in user."""

from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from .models import Server


def servers_for_user(request: HttpRequest) -> dict[str, Any]:
    if not request.user.is_authenticated:
        return {"user_servers": []}
    return {
        "user_servers": list(
            Server.objects.filter(members=request.user).order_by("name"),
        ),
    }
