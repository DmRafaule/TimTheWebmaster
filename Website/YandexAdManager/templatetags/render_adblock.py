from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag(takes_context=True, name="render_adblock")
def render_adblock(context, adblock, unificator=None):
    template_name = getattr(adblock, "adblock_template", "YandexAdManager/admanager_element_default.html")
    return render_to_string(template_name, {
        "adblock": adblock,
        "unificator": unificator,
        **context.flatten()
    })