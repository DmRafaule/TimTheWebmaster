from django import template
from django.utils.translation import gettext as _


register = template.Library()


@register.filter
def durationToStr(td):

    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = _("{days}Д").format(days=days) + ' ' if days else ''
    hours_str = _("{hours}Ч").format(hours=hours) + ' ' if hours else ''
    minutes_str = _("{minutes}М").format(minutes=minutes) + ' ' if minutes else ''
    seconds_str = _("{seconds}С").format(seconds=seconds) if seconds and not hours_str else ''

    return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
