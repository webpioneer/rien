from django.dispatch import receiver
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.views import render
from mezzanine.utils.sites import current_site_id


from gigs.signals import gig_is_validated
from marketing.forms import SubscribeForm
from searchapp.models import GigSearch
from searchapp.search import store, gig_searches_similar_to_gig

def subscribe_email(request, template_name = 'gigs/index.html'):
	if request.method == 'POST' and request.is_ajax():
		subscribe_form = SubscribeForm(request.POST)
		print request.POST
		if subscribe_form.is_valid():
			post_data = subscribe_form.cleaned_data
			what = request.POST.get('what','')
			location = request.POST.get('location','')
			gig_types_string = request.POST.get('gig_types_string','')
			remote = request.POST.get('remote','')
			gig_search = store(request, what, location, gig_types_string, remote)
			gig_search.subscribed_user = post_data['email']
			gig_search.save()
			message = '<strong>Subscribed</strong>We will be sending you matching jobs as they come in. Good luck'
    		response = simplejson.dumps({
               'message' :  message.lower(),
               })
    		return HttpResponse(response, content_type='application/javascript')
	else:
		subscribe_form = SubscribeForm()

	context = {
		'subscribe_form' : subscribe_form,
	}
	return render(request, template_name, context)

@receiver(gig_is_validated, sender = 'post_job')
@receiver(gig_is_validated, sender = 'response_change')
def email_subscribed_users(sender, **kwargs):
	"""
	Subscribed users to gig search similar to the validated
	gig are notified
	"""
	gig = kwargs['gig']
	print 'send notification to subscribed_user'
	#gig_searches = gig_searches_similar_to_gig(gig)
	# send email/ notification to subscribed users