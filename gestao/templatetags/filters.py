import collections

from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter
def hash(h, key):
    return h[key]