from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('searchapp.views',
	url("^/$", 'search_objects', {"template_name": "searchapp/results.html"}, name = "find_jobs"),
)
