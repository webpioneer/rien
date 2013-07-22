from django.conf.urls.defaults import patterns, url

from mezzanine.core.views import direct_to_template

urlpatterns = patterns('',
	url("^about/$", direct_to_template, {"template": "marketing/about.html"}, name = "about"),
)

