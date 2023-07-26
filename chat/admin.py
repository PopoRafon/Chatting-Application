from django.contrib import admin
from .models import Chat, ChatMessage, Channel, ChannelMessage


admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Channel)
admin.site.register(ChannelMessage)
