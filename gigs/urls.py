from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gigs.views',
	url("^$", 'all_gigs', {"template_name": "gigs/index.html"}, name = "home"),
	#url("^find_jobs/$", 'find_jobs', name = "find_jobs"),
	url("^job/(?P<slug>[-\w]+)/$", 'get_gig', {"template_name": "gigs/get_gig.html"}, name="get_gig"),
    url('post_job/$','post_job',{'template_name':'gigs/post_job.html'}, name = 'post_job'),
    # Company urls
    url('company/profile/(?P<slug>[-\w]+)/$', 'company_profile', {'template_name':'gigs/company/company_profile.html'}, name = 'company_profile'),
    url('company/listings/$', 'company_listings', {'template_name':'gigs/company/company_listings.html'}, name = 'company_listings'),
    url('company/infos/$', 'company_infos', {'template_name':'gigs/company/company_infos.html'}, name = 'company_infos'),
)

urlpatterns += patterns('gigs.utils.views',
    #returns gig info for cart.html page using ajax
    url('get_gig_info/(?P<sku>[-\w]+)/$','get_gig_info', name = 'get_gig_info'),
)
