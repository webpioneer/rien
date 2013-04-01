from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gigs.views',
	url("^$", 'all_gigs', {"template_name": "gigs/index.html"}, name="home"),
	url("^job/(?P<slug>[-\w]+)/$", 'get_gig', {"template_name": "gigs/get_gig.html"}, name="get_gig"),
    url('post_job/$','post_job',{'template_name':'gigs/post_job.html'}, name = 'post_job'),
)
