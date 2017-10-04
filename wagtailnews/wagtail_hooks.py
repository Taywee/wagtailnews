from django.conf.urls import include, url
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.core.urlresolvers import reverse
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.search import SearchArea
from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.forms import collection_member_permission_formset_factory

from . import urls
from .menu import NewsMenuItem
from .models import NEWSINDEX_MODEL_CLASSES
from .permissions import user_can_edit_news


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^news/', include(urls)),
    ]


@hooks.register('construct_main_menu')
def construct_main_menu(request, menu_items):
    if user_can_edit_news(request.user):
        menu_items.append(NewsMenuItem())


class NewsItemSearchArea(SearchArea):
    """Admin search for news items."""
    def __init__(self, **kwargs):
        super(NewsItemSearchArea, self).__init__(
            _('News'), urlresolvers.reverse('wagtailnews:search'),
            classnames='icon icon-grip', order=250, **kwargs)

    def is_shown(self, request):
        return user_can_edit_news(request.user)


@hooks.register('register_admin_search_area')
def register_news_search():
    """Register news search."""
    return NewsItemSearchArea()


@hooks.register('register_permissions')
def newsitem_permissions():
    newsitem_models = [model.get_newsitem_model()
                       for model in NEWSINDEX_MODEL_CLASSES]
    newsitem_cts = ContentType.objects.get_for_models(*newsitem_models).values()
    return Permission.objects.filter(content_type__in=newsitem_cts)


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('js/news_chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>\n',
        ((filename, ) for filename in js_files)
    )
    urls = format_html(
        '<script>window.chooserUrls.newsChooser = "{}";</script>',
        reverse('wagtailnews:chooser'))
    return js_includes + urls

# Store strong ref just in case wagtail ever decides to switch hooks to weak references
_PERMISSIONS_HOOKS = []

def _get_register_newsitem_permissions_panel(cls):
    def register_newsitem_permissions_panel():
        content_type = ContentType.objects.get_for_model(cls)

        return collection_member_permission_formset_factory(
            # Delete is automatically covered in change.
            cls,
            [
                ('add_newsitem', _("Create"), _("Create any newsitem")),
                ('change_newsitem', _("Edit"), _("Edit/delete any newsitem")),
                ],
            'wagtailnews/permissions/includes/newsitem_permissions_formset.html'
            )
    return register_newsitem_permissions_panel

def register_all_permissions():
    # Restricted to only being called once
    if not _PERMISSIONS_HOOKS:
        for cls in NEWSINDEX_MODEL_CLASSES:
            hook = _get_register_newsitem_permissions_panel(cls.get_newsitem_model())
            _PERMISSIONS_HOOKS.append(hook)
            hooks.register('register_group_permission_panel', hook)
