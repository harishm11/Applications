from django.contrib.auth.models import Group, User


def selected_group(request):
    selected_group_id = request.session.get('selected_group_id')
    # existing_groups = list(
    #         request.user.groups.values_list('name', flat=True))
    # request.session['session_groups'] = existing_groups
    if selected_group_id:
        try:
            selected_group = Group.objects.get(id=selected_group_id)
            request.user.groups.clear()  # Clear existing group memberships
            request.user.groups.add(selected_group)  # Add the selected group

            # user = request.user

            # # Iterate through the user's groups
            # for group in user.groups.all():
            #     print(f"Group: {group.name}")

            #     # Iterate through the permissions of the group
            #     for permission in group.permissions.all():
            #         print(
            #             f"  Permission: {permission.codename} ({permission.name})")
        except Group.DoesNotExist:
            pass

    return {}
