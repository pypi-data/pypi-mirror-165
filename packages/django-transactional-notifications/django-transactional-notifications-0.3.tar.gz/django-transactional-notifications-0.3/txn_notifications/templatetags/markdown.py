import re

from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
from bs4 import BeautifulSoup

register = template.Library()


@register.filter
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=["markdown.extensions.fenced_code"])


@register.filter
@stringfilter
def simple_text(value):
    """Converts a markdown string to plaintext"""

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(value)

    # remove code snippets
    html = re.sub(r"<pre>(.*?)</pre>", " ", html)
    html = re.sub(r"<code>(.*?)</code >", " ", html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = "".join(soup.findAll(string=True))

    return text
