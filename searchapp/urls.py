from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(
	'searchapp.views',
	#url("^/$", 'search_objects', {"template_name": "searchapp/results.html"}, name = "find_jobs"),
	url("^/$", 'search_objects', {"template_name": "gigs/index.html"}, name = "find_jobs"),
	#url("^/$", 'gigs.views.all_gigs', {"template_name": "gigs/index.html"}, name = "find_jobs"),
)
