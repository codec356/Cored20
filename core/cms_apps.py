from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


@apphook_pool.register
class CoreApphook(CMSApp):
    app_name = "core"  # must match the application namespace
    name = "CoreHook"

    def get_urls(self, page=None, language=None, **kwargs):
        return ['core.urls']  # replace this with the path to your application's URLs module
