"""
Default settings for the ``mezzanine.blog`` app. Each of these can be
overridden in your project's settings module, just like regular
Django settings. The ``editable`` argument for each controls whether
the setting is editable via Django's admin.

Thought should be given to how a setting is actually used before
making it editable, as it may be inappropriate - for example settings
that are only read during startup shouldn't be editable, since changing
them would require an application reload.
"""

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

register_setting(
    name="SITE_ADDRESS",
    label=_("Address *"),
    description=_("Site address"),
    editable=True,
    default= '836 Sierra Vista Mountain View Ca',
)

register_setting(
    name="SITE_EMAIL",
    label=_("A dedicated email address to the side"),
    description=_("eg. hello@jobconnector.com"),
    editable=True,
    default= 'hello@jobconnector.com',
)

register_setting(
    name="SITE_HERO_UNIT",
    label=_("Site Hero unit *"),
    description=_("site hero unit"),
    editable=True,
    default= '',
)

register_setting(
    name="SITE_LANGUAGE",
    label=_("Site Language *"),
    description=_("The site language"),
    editable=True,
    default= 'en',
)

register_setting(
    name="SITE_COUNTRY",
    label=_("Site Country *"),
    description=_("country matches a country name or a two letter ISO 3166-1 country code \
        refer to : https://developers.google.com/maps/documentation/geocoding/ and http://en.wikipedia.org/wiki/CcTLD"),
    editable=True,
    default= 'us',
)

register_setting(
    name="SITE_OPERATOR",
    label=_("Site Operator"),
    description=_("Responsible for customer service"),
    editable=True,
    default= 'Mike',
)

register_setting(
    name="SITE_PHONE",
    label=_("Phone *"),
    description=_("Site phone"),
    editable=True,
    default= '',
)

register_setting(
    name="SITE_STATE",
    label=_("SITE STATE"),
    description=_("eg. Florida / Eastern Time"),
    editable=True,
    default= '',
)

register_setting(
    name="PAYPAL_USER",
    label=_("Paypal User *"),
    description=_("Paypal user"),
    editable=True,
    default= 'contact_api1.djangojobs.org',
)

register_setting(
    name="PAYPAL_PASSWORD",
    label=_("Paypal password *"),
    description=_("Paypal password"),
    editable=True,
    default= 'U4E2VWF3KWU9A2XX',
)

register_setting(
    name="PAYPAL_SIGNATURE",
    label=_("Paypal signature *"),
    description=_("Paypal signature"),
    editable=True,
    default= 'AR6gDcq86QpriE9SFyYUOIjn4mByANdDCi9Tmu.OemEkbdE6g-dDyWVO',
)
register_setting(
    name="TWITTER_ACCOUNT",
    label=_("Site twitter account *"),
    description=_("Twitter account link"),
    editable=True,
    default= 'http://twitter.com',
)

register_setting(
    name="TWITTER_CONSUMER_KEY",
    label=_("Site twitter consumer key *"),
    description=_("Twitter consumer key"),
    editable=True,
    default= '',
)

register_setting(
    name="TWITTER_CONSUMER_SECRET",
    label=_("Site twitter consumer secret *"),
    description=_("Twitter consumer secret"),
    editable=True,
    default= '',
)

register_setting(
    name="TWITTER_ACCESS_TOKEN",
    label=_("Site twitter access token *"),
    description=_("Twitter access token"),
    editable=True,
    default= '',
)

register_setting(
    name="TWITTER_ACCESS_TOKEN_SECRET",
    label=_("Site twitter access token secret *"),
    description=_("Twitter access token secret"),
    editable=True,
    default= '',
)

register_setting(
    name="SITE_FACEBOOK_ACCOUNT",
    label=_("Site facebook account *"),
    description=_("Facebook account link"),
    editable=True,
    default= 'http://facebook.com',
)

register_setting(
    name="SITE_LINKEDIN_ACCOUNT",
    label=_("Site linkedin account *"),
    description=_("Linkedin account link"),
    editable=True,
    default= 'http://linkedin.com',
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=("SITE_ADDRESS", "SITE_COUNTRY", "SITE_EMAIL", "SITE_HERO_UNIT", "SITE_LANGUAGE", "SITE_OPERATOR",
        "SITE_PHONE", "SITE_STATE",   
        "SHOP_PAYMENT_STEP_ENABLED","PAYPAL_USER", "PAYPAL_PASSWORD", "PAYPAL_SIGNATURE", 
        "SITE_TWITTER_ACCOUNT", "SITE_FACEBOOK_ACCOUNT",
        "SITE_LINKEDIN_ACCOUNT"),
    append=True,
)

