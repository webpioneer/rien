from django.conf import settings
from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.views import render, paginate

from gigs.models import GigType

from searchapp.forms import GigSearchForm
from searchapp.models import GigSearch
from searchapp.search import store, get_results

def get_gig_types_to_display(list1, list2):
	delta = len (list1) - len(list2)
	if delta == 2:
		return _('(%s)' % ' & '.join([GigType.objects.get(id = item).type for item in list2]))
	elif delta == 3:
		return _('(except %s)' % GigType.objects.get(id = list2[0]).type)
	elif delta == 4:
		return ''

def search_objects(request, template_name = 'gigs/index.html'):
#def search_objects(request, template_name = 'searchapp/index.html'):
	gig_search_form = GigSearchForm(request.POST)
	#if request.method == 'POST' and request.is_ajax():
	if request.method == 'POST':
		if gig_search_form.is_valid():
			what = gig_search_form.cleaned_data['what'].strip()
			location = gig_search_form.cleaned_data['location'].strip()

			remote = True if request.POST.get('remote') else False
			#gig_types = gig_search_form.cleaned_data['gig_types']
			
			#gig_types = request.POST['gig_types']
			#print 'gig types : %s ' % gig_types
			#page = request.POST['page']
						
	#elif request.method == 'GET' and request.is_ajax():
	elif request.method == 'GET':
		what = request.GET.get('what', '')
		location = request.GET.get('location', '')
		page = request.GET.get['page']
		gig_types = request.GET.get('gig_types', '')

	if 'searchapp' in settings.INSTALLED_APPS:
		#store(request, what, location, gig_types)
		pass
	#response = simplejson.dumps({
	#			'results' :  get_results(what, location, page, gig_types),
	#			'what' : what.capitalize(),
	#			'location' : location.title(),
	#			})
	#http_response = HttpResponse(response, content_type='application/javascript')

	gig_types_string = '%s %s %s %s' % (request.POST.get('Full-time',''),
		request.POST.get('Internship',''),
		request.POST.get('Contract',''),
		request.POST.get('Freelance',''),
		)

	gig_types = GigType.objects.all()

	gig_types_list = [ gig_type.id for gig_type in gig_types if str(gig_type.id) not in gig_types_string]
 
	
 	results = get_results(what, location, request.GET.get("page", 1), gig_types_list, remote)
	results = paginate(results, request.GET.get("page", 1),
                          settings.GIGS_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
	
	
	context = {
		'gigs' : results,
		'what' : what.capitalize(),
		'location' : location.capitalize(),
		'gig_search_form' : gig_search_form,
		'gig_types' : gig_types,
		'gig_types_string' : gig_types_string,
		'gig_types_list' : gig_types_list,
		'gig_types_to_display' : get_gig_types_to_display(gig_types, gig_types_list),
		'remote' : remote,
	}

	return render(request, template_name, context)

		

