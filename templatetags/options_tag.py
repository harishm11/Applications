from django import template

register = template.Library()


@register.filter
def filter_option_value(selected_coverages, OptionValue):
    return OptionValue in selected_coverages
