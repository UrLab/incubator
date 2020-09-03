import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeText

register = template.Library()


@register.filter(is_safe=False, name='markdown')
@stringfilter
def my_markdown(value):
    extensions = ["nl2br", "extra", "codehilite", "toc", "sane_lists"]

    html = mark_safe(markdown.markdown(
        value,
        extensions=extensions,
        safe_mode='escape',
        enable_attributes=False,
        output_format="html5"
    ))
    return SafeText(html)


@register.filter(is_safe=False, name='unsafeMarkdown')
@stringfilter
def my_markdown(value):
    extensions = ["nl2br", "extra", "codehilite", "toc", "sane_lists"]

    html = mark_safe(markdown.markdown(
        value,
        extensions=extensions,
        safe_mode=False,
        enable_attributes=False,
        output_format="html5"
    ))
    return SafeText(html)
