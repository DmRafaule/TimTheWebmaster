from django import template

register = template.Library()

@register.filter
def checkLocation(locations, name):
    """Возвращает первый элемент из locations с атрибутом linklocation_name равным name, иначе None."""
    return next((loc for loc in locations if loc.linklocation_name == name), None)