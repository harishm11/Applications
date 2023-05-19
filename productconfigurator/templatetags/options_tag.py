from urllib.parse import urlencode
from django import template

register = template.Library()


@register.simple_tag
def url_with_query(url, **kwargs):
    query_params = urlencode(kwargs)
    if query_params:
        return f"{url}&{query_params}"
    return url
