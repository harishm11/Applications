from django import template

register = template.Library()


@register.filter
def filter_option_value(selected_coverages, option_value):
    return option_value in selected_coverages
