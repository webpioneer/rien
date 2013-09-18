from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
	url("^/$", 'feedb.views.submit_feedback', {"template_name": "feedb/submit_feedback.html"}, name = "submit_feedback"),
	url("^/(?P<app_name>[-\w]+)/(?P<model_name>[-\w]+)/(?P<id>[-\w]+)$", 'feedb.views.submit_feedback', 
		{"template_name": "feedb/submit_feedback.html"}, name = "submit_feedback"),
)

