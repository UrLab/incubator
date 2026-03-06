import markdown
import nh3

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "p",
    "br",
    "hr",
    "a",
    "img",
    "strong",
    "em",
    "b",
    "i",
    "u",
    "s",
    "del",
    "ins",
    "sub",
    "sup",
    "ul",
    "ol",
    "li",
    "blockquote",
    "pre",
    "code",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
    "div",
    "span",
    "dl",
    "dt",
    "dd",
    "abbr",
}

ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "img": {"src", "alt", "title"},
    "abbr": {"title"},
    "td": {"colspan", "rowspan"},
    "th": {"colspan", "rowspan"},
    "code": {"class"},
    "div": {"class"},
    "span": {"class"},
    "pre": {"class"},
}


def _render_markdown(value):
    """Render markdown to HTML and sanitize the output."""
    extensions = ["nl2br", "extra", "codehilite", "toc", "sane_lists"]
    raw_html = markdown.markdown(value, extensions=extensions, output_format="html5")
    return nh3.clean(
        raw_html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
    )


@register.filter(is_safe=False, name="markdown")
@stringfilter
def safe_markdown(value):
    return mark_safe(_render_markdown(value))


@register.filter(is_safe=False, name="unsafeMarkdown")
@stringfilter
def unsafe_markdown(value):
    """Render markdown to sanitized HTML.

    Despite the name, this filter uses the same sanitized rendering path as the
    ``markdown`` filter via ``_render_markdown``. It is retained for backwards
    compatibility with existing templates that reference ``unsafeMarkdown``.
    """
    return mark_safe(_render_markdown(value))
