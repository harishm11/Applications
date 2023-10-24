from django import template
from django.contrib.auth.models import Group
register = template.Library()


@register.filter
def has_permission(perms, app_and_permission):
    app, permission = app_and_permission.split('.')
    group = Group.objects.get(name=perms.user.groups.all()[0])
    group_permissions = group.permissions.all()
    for group_permission in group_permissions:
        if group_permission.codename == permission:
            # print(group_permission.codename)
            # print(permission)
            return True

    return False
