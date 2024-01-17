from django import template

register = template.Library()


@register.filter
def get_attribute(obj, attr):
    return getattr(obj, attr)


@register.filter(name='verbose_name')
# Gets the name of the passed in field on the passed in object
def verbose_name(the_object, the_field):
    return the_object._meta.get_field(the_field).verbose_name
