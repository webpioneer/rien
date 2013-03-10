from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('gigs.views',
    url('post_job/$','post_job',{'template_name':'gigs/post_job.html'}, name = 'post_job'),
)
