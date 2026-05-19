from django.contrib import admin

from .models import Attachment, DirectMessage, DirectMessageThread, Message, Reaction


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("puid", "channel", "author", "created_at", "deleted")
    list_filter = ("deleted",)
    search_fields = ("content", "author__username", "channel__name", "puid")
    autocomplete_fields = ["author", "channel"]


admin.site.register(Reaction)
admin.site.register(Attachment)
admin.site.register(DirectMessageThread)
admin.site.register(DirectMessage)
