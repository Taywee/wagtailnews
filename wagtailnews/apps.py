from django.apps import AppConfig

class WagtailNewsConfig(AppConfig):
    '''Simply registers hooks'''
    name = 'wagtailnews'
    def ready(self):
        from . import wagtail_hooks
        wagtail_hooks.register_all_permissions()
