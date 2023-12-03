from django.utils import timezone
from django import template

register = template.Library()


@register.filter
def formatted_time(message):
    message_creation_date = message.date()
    today = timezone.now().date()
    yesterday = timezone.now().date() - timezone.timedelta(1)

    if message_creation_date == today:
        return f'Today at {message.hour:02d}:{message.minute:02d}'
    elif message_creation_date == yesterday:
        return f'Yesterday at {message.hour:02d}:{message.minute:02d}'
    else:
        return f'{message_creation_date} {message.hour:02d}:{message.minute:02d}'
