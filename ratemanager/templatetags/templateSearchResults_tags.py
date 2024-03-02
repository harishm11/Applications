from django import template
from ratemanager.views.HelperFunctions import checkTemplateCreateButtonEnable

register = template.Library()


@register.filter(name='checkTemplateCreateEnable')
# Gets the name of the passed in field on the passed in object
def checkTemplateCreateEnable(the_object):
    status = checkTemplateCreateButtonEnable(the_object)
    return status
