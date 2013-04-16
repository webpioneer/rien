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
    name="ADDRESS",
    label=_("Address"),
    description=_("Site address"),
    editable=True,
    default= '836 Sierra Vista Mountain View Ca',
)

register_setting(
    name="PHONE",
    label=_("Phone"),
    description=_("Site phone"),
    editable=True,
    default= '9202151540',
)

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=("ADDRESS", "PHONE"),
    append=True,
)

