from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from wagtailnews.models import NEWSINDEX_MODEL_CLASSES
from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.forms import collection_member_permission_formset_factory

def _get_register_newsitem_permissions_panel(cls):
    def register_newsitem_permissions_panel():
        content_type = ContentType.objects.get_for_model(cls)

        # Make sure permissions exist as well
        # This may not be necessary; try it without first
        #Permission.objects.get_or_create(
        #    content_type=content_type,
        #    codename='change_newsitem',
        #    defaults={'name': 'Can change news items'}
        #    )

        return collection_member_permission_formset_factory(
            cls,
            [
                ('add_newsitem', _("Create"), _("Create any newsitem")),
                ('change_newsitem', _("Edit"), _("Edit any newsitem")),
                ('delete_newsitem', _("Delete"), _("Delete any newsitem")),
                ],
            'wagtailnews/permissions/includes/newsitem_permissions_formset.html'
            )
    return register_newsitem_permissions_panel

# Store strong ref just in case wagtail ever decides to switch hooks to weak references
_HOOKS = []

def newsindex(cls):
    NEWSINDEX_MODEL_CLASSES.append(cls)
    # Register the formset for each newsitem type
    hook = _get_register_newsitem_permissions_panel(cls.get_newsitem_model())
    _HOOKS.append(hook)
    hook.register('register_group_permission_panel')(hook)
    return cls
