from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
	url("^/email_resume/(?P<attach>[-\w]+)$", 'utils_app.views.email_resume', {'template_name' : 'gigs/company/application_detail.html'} , name = "email_resume"),
	url("^/people/$", 'utils_app.views.people', {'template_name' : 'utils_app/people.html'} , name = "people"),
)

