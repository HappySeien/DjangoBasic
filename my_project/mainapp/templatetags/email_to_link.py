from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def email_to_link(str_email):
    return mark_safe(f'<a href="mailto:{str_email}">{str_email}</a>')
