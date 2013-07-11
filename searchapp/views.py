from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson

from mezzanine.utils.views import render

from searchapp.forms import GigSearchForm
from searchapp.models import GigSearch
from searchapp.search import store, get_results

def search_objects(request, template_name = 'searchapp/results.html'):
	gig_search_form = GigSearchForm(request.POST)
	if request.method == 'POST' and request.is_ajax():
		if gig_search_form.is_valid():
			print 'form is valid'
			what = gig_search_form.cleaned_data['what']
			location = gig_search_form.cleaned_data['location']
			#gig_types = gig_search_form.cleaned_data['gig_types']
			
			gig_types = request.POST['gig_types']
			print 'gig types : %s ' % gig_types
			page = request.POST['page']
			print what, location
						
	elif request.method == 'GET' and request.is_ajax():
		what = request.GET.get('what', '')
		location = request.GET.get('location', '')
		page = request.GET['page']
		gig_types = request.GET.get('gig_types', '')

	if 'searchapp' in settings.INSTALLED_APPS:
		#store(request, what, location, gig_types)
		pass
	response = simplejson.dumps({
				'results' :  get_results(what, location, page, gig_types),
				'what' : what.capitalize(),
				'location' : location.title(),
				})
	return HttpResponse(response, content_type='application/javascript')

		

