from django import template

register = template.Library()

@register.filter
def get_coverage_name(coverage_option):
    return coverage_option.CoverageName

@register.filter
def get_option_value(coverage_option):
    return coverage_option.OptionValue
