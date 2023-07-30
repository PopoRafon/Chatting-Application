from .models import Chat
from channels.db import database_sync_to_async


@database_sync_to_async
def has_chat_access(user, chat_id):
    try:
        chat = Chat.objects.get(id=chat_id)
        return user in chat.users.all()
    except Chat.DoesNotExist:
        return False
