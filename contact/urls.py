from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
	url("^/$", 'contact.views.contact', {"template_name": "contact/contact.html"}, name = "contact"),
)

