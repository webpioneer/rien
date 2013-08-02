from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gigs.views',
	url("^$", 'all_gigs', {"template_name": "gigs/index.html"}, name = "home"),
	#url("^find_jobs/$", 'find_jobs', name = "find_jobs"),
	url("^job/(?P<slug>[-\w]+)/$", 'get_gig', {"template_name": "gigs/get_gig.html"}, name="get_gig"),
    url('post_job/$','post_job',{'template_name':'gigs/post_job.html'}, name = 'post_job'),
    # Company urls
    url('company/profile/(?P<slug>[-\w]+)/$', 'company_profile', {'template_name':'gigs/company/company_profile.html'}, name = 'company_profile'),
    url('profile/listings/$', 'company_listings', {'template_name':'gigs/company/company_listings.html'}, name = 'company_listings'),
    url('profile/infos/$', 'company_infos', {'template_name':'gigs/company/company_infos.html'}, name = 'company_infos'),
    url('company/listing/(?P<slug>[-\w]+)/$', 'view_listing', {'template_name':'gigs/company/view_listing.html'}, name = 'view_listing'),
    url('application/(?P<message_id>[\d]+)/$','application_detail', {'template_name':'gigs/company/application_detail.html'}, name = 'application_detail'),
    url('application/(?P<sign>[-\w]+)/(?P<id>[-\w]+)/$','application_follower', {'template_name':'gigs/company/application_detail.html'}, name = 'application_follower'),
    url('application/accept/$', 'application_accept', name = 'application_accept'),
    # Apply
    url('profile/applications/$', 'applier_applications', {'template_name':'gigs/applier/applier_applications.html'}, name = 'applier_applications'),
    #url('apply/(?P<gig_slug>[-\w]+)/$','apply',{'template_name':'gigs/apply.html'}, name = 'apply'),
    url('apply/(?P<gig_slug>[-\w]+)/$','apply',{'template_name':'gigs/get_gig.html'}, name = 'apply'),
    url('application/reply/(?P<application_id>[-\w]+)$', 'reply_to_apply', {'template_name':'gigs/company/application_detail.html'}, name = 'reply_to_apply'),
    # Profile
    #url('profile/account/password_reset$', django.contrib.auth.views.password_reset, {'template_name':'gigs/account.html'}, name = 'password_reset'),

)

urlpatterns += patterns('gigs.utils.views',
    #returns gig info for cart.html page using ajax
    url('get_gig_info/(?P<sku>[-\w]+)/$','get_gig_info', name = 'get_gig_info'),
)


urlpatterns += patterns('',
    #Profile
    url(r'^account/$', 'gigs.views.account', {'template_name':'gigs/account.html'} ,name='account'),
    # profile password change
    url(r'^account/password_change/$', 'django.contrib.auth.views.password_change', {'template_name':'gigs/company/account_password_change.html'}, name='password_change'),
    url(r'^account/password_change/done/$', 'django.contrib.auth.views.password_change_done', {'template_name':'gigs/company/account_password_change_done.html'}, name='password_change_done'),
    # Update profile
    url(r'^account/update-profile/$', 'mezzanine.accounts.views.profile_update', {'template':'gigs/company/account_personal.html'} ,name='profile_update'),
    # Account notifications
    url(r'^account/notifications$', 'gigs.views.set_notifications', {'template_name':'gigs/company/account_notifications.html'} ,name='account_notifications'),
)