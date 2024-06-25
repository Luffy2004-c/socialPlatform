from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()


@register.filter
def time_ago(value):
    if not value:
        return ""
    try:
        now = timezone.now()
        difference = now - value
        if difference.days > 0:
            return f"{difference.days} days ago"
        elif difference.seconds <= 60:
            return "just now"
        elif difference.seconds < 3600:
            minutes = difference.seconds // 60
            return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
        else:
            hours = difference.seconds // 3600
            return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    except Exception as e:
        return value
