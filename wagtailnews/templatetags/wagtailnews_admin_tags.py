from django.core.urlresolvers import reverse
from django.template.library import Library
from django.utils.html import format_html, mark_safe
from django.utils.translation import ugettext as _

register = Library()


@register.simple_tag()
def newsitem_status(newsitem, link=True):
    buttons = []
    output = []
    if newsitem.live:
        buttons.append({
            'href': newsitem.url,
            'primary': True,
            'text': _('live'),
        })
    if newsitem.has_unpublished_changes or not newsitem.live:
        buttons.append({
            'href': reverse('wagtailnews:view_draft', kwargs={
                'pk': newsitem.newsindex.pk, 'newsitem_pk': newsitem.pk,
            }),
            'primary': False,
            'text': _('draft'),
        })

    if link:
        for button in buttons:
            output.append(format_html(
                '<a href="{}" target="_blank" class="{}">{}</a>',
                button['href'],
                'status-tag primary' if button['primary'] else 'status-tag',
                button['text']))
    else:
        for button in buttons:
            output.append(format_html(
                '<span class="{}">{}</span>',
                'status-tag primary' if button['primary'] else 'status-tag',
                button['text']))

    return mark_safe(' + '.join(output))

@register.simple_tag(takes_context=True)
def check_permissions(context, perm, newsitem):
    policy = context['policy']
    user = context['request'].user
    print('running policy {} for user {} perm {} and newsitem {}'.format(policy, user, perm, newsitem))
    val = policy.user_has_permission_for_instance(user, perm, newsitem)
    print('returning {}'.format(val))
    return val
