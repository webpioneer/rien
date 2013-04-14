from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson

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
			print gig_types
			page = request.POST['page']
			print what, location
						
	elif request.method == 'GET' and request.is_ajax():
		what = request.GET['what']
		location = request.GET['location']
		page = request.GET['page']
		gig_types = request.GET['gig_types']
	store(request, what, location, gig_types)
	response = simplejson.dumps({
				'results' :  get_results(what, location, page),
				'what' : what,
				'location' : location,
				})
	return HttpResponse(response, content_type='application/javascript')

		

