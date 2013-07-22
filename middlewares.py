import re
from django.utils import translation

from mezzanine.conf import settings
from mezzanine.utils.sites import current_site_id

class LocaleSelectorMiddleware(object):
    "Set the language code for the request depending on what host we're requesting."

    #these constants must match what the sites as they are defined in the django_site table
    #LOCALHOST = 1
    #FR = 3

    #languages = { LOCALHOST: 'en', FR: 'fr', }
    locales = { 
        3 : 'fr_FR.UTF-8', # French
        4 : 'en_GB.UTF-8', # British
        5 : 'sv_SE.UTF-8', # Swedish
    }

    def process_request(self, req):
        if self.localize_request(req):
            language = self.get_language()
            translation.activate(language)
            req.LANGUAGE_CODE = translation.get_language()
            # set SHOP_CURRENCY_LOCALE
            settings.SHOP_CURRENCY_LOCALE =self.locales.get(current_site_id(),'')
            req.SHOP_CURRENCY_LOCALE = self.locales.get(current_site_id(),'')

    def get_language(self):
        #sid = current_site_id()
        #if self.languages.get(sid):
        #    return self.languages[sid]
        #else:
        #    logger.error("Couldn't get language for site id: %s" % sid)
        #    return 'en'
        return getattr(settings, 'SITE_LANGUAGE', 'en')

    def localize_request(self, req):
        for no_rewrite_path in ['^/admin/*']:
            if re.match(no_rewrite_path, req.path):
                return False
        return True