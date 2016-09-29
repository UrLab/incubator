from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_if_contains(context, url_part):
    request = context['request']
    if url_part in request.path:
        return "active"
    else:
        return ""
