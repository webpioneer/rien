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
    name="LANGUAGE",
    label=_("Site Language *"),
    description=_("The site language"),
    editable=True,
    default= 'en',
)

register_setting(
    name="COUNTRY",
    label=_("Site Country *"),
    description=_("country matches a country name or a two letter ISO 3166-1 country code \
        refer to : https://developers.google.com/maps/documentation/geocoding/ and http://en.wikipedia.org/wiki/CcTLD"),
    editable=True,
    default= 'us',
)

register_setting(
    name="ADDRESS",
    label=_("Address *"),
    description=_("Site address"),
    editable=True,
    default= '836 Sierra Vista Mountain View Ca',
)

register_setting(
    name="PHONE",
    label=_("Phone *"),
    description=_("Site phone"),
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
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=("ADDRESS", "PHONE", "LANGUAGE", "COUNTRY", "SHOP_PAYMENT_STEP_ENABLED",
        "PAYPAL_USER", "PAYPAL_PASSWORD", "PAYPAL_SIGNATURE"),
    append=True,
)

