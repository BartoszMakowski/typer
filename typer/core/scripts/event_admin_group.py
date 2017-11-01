from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from typer.core.models import Event

content_type = ContentType.objects.get_for_model(Event)
event_close_permissions = Permission.objects.get(codename='can_close', content_type=content_type)
event_add_permissions = Permission.objects.get(name='Can add event', content_type=content_type)

group, created = Group.objects.get_or_create(name='Event admins')
group.permissions.set((event_close_permissions, event_add_permissions))
group.save()