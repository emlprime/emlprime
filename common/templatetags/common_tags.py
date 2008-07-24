from django import template
from django.conf import settings

register = template.Library()

@register.filter

@register.inclusion_tag("footer.html")
def footer():
    return settings.FOOTER_DATA

