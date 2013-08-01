from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('faqs.views',
	url("^/$", 'faqs_list', {"template_name": "faqs/faqs_list.html"}, name = "faqs"),
)

