import re
from django.utils import translation

from mezzanine.utils.sites import current_site_id

class LocaleSelectorMiddleware(object):
    "Set the language code for the request depending on what host we're requesting."

    #these constants must match what the sites as they are defined in the django_site table
    LOCALHOST = 1
    FR = 3

    languages = { LOCALHOST: 'en', FR: 'fr', }

    def process_request(self, req):
        if self.localize_request(req):
            language = self.get_language()
            print "language :" +language
            translation.activate(language)
            req.LANGUAGE_CODE = translation.get_language()
            print "req.LANGUAGE_CODE" + req.LANGUAGE_CODE

    def get_language(self):
        sid = current_site_id()
        if self.languages.get(sid):
            return self.languages[sid]
        else:
            #logger.error("Couldn't get language for site id: %s" % sid)
            print "Couldn't get language for site id: %s" % sid
            return 'en'

    def localize_request(self, req):
        for no_rewrite_path in ['^/admin/*']:
            if re.match(no_rewrite_path, req.path):
                return False
        return True