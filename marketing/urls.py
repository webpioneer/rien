from django.conf.urls.defaults import patterns, url

from mezzanine.core.views import direct_to_template

from marketing.feeds import GigFeed

urlpatterns = patterns('',
	url("^about/$", direct_to_template, {"template": "marketing/about.html"}, name = "about"),
	# generate feed (?P<slug>[-\w]+)/
	url("^jobs/feed/$", GigFeed(), name = 'jobs_feed'),
	url("^jobs/feed/(?P<what>[-\w]+)/$", GigFeed()),
	url("^jobs/feed/(?P<what>[-\w]+)/(?P<location>[-\w ]+)/$", GigFeed()),
	url("^jobs/feed/(?P<what>[-\w]+)/(?P<location>[-\w ]+)/(?P<gig_types>[-\w ]+)/(?P<remote>[-\w ]+)/$", GigFeed()),
)

urlpatterns += patterns('marketing.views',
	# subscribe to email
	url("^subscribe/email/$", 'subscribe_email', name = 'subscribe_email'),
)