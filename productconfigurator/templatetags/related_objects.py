from django import template

register = template.Library()


@register.simple_tag
def related_objects(obj, field_name):
    try:
        related_manager = getattr(obj, field_name)
        return related_manager.all()
    except AttributeError:
        return None
