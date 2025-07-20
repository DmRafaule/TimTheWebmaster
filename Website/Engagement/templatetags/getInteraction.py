from django import template
from Engagement.models import Interaction

register = template.Library()


@register.filter(name='getInteraction')
def getInteraction(url):
    interaction_qs = Interaction.objects.filter(url=url)
    if len(interaction_qs) > 0:
        return interaction_qs[0]
    else:
        return Interaction(url='-empty-')