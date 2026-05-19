from django.contrib import admin

from .models import Channel, Membership, Server


class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 0


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0
    autocomplete_fields = ["user"]


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "is_public", "created_at")
    list_filter = ("is_public",)
    search_fields = ("name", "slug", "puid")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ChannelInline, MembershipInline]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "server", "kind", "position")
    list_filter = ("kind",)
    search_fields = ("name", "server__name", "puid")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "server", "role", "joined_at")
    list_filter = ("role",)
    autocomplete_fields = ["user", "server"]
