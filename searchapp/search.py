from itertools import chain

from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.template.defaultfilters import date


from mezzanine.utils.sites import current_site_id

from gigs.models import Gig, GigType
from searchapp.models import GigSearch

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
				'of', 'on', 'or', 'that', 'the', 'to', 'with']

def store(request, what, location, gig_types):
	gig_terms = GigSearch()
	if len(what) > 2:
		gig_terms.what = what
	gig_terms.location = location
	#gig_terms.longitude = longitude
	#gig_terms.latitude = latitude
	#gig_terms.area_level1 = area_level1
	#gig_terms.area_level2 = area_level2
	gig_terms.ip_address = request.META.get('REMOTE_ADDR','')
	if request.user.is_authenticated():
		gig_terms.user = request.user
	#gig_terms.is_onsite = is_onsite
	if 'remote' in gig_types:
		gig_terms.is_onsite = True
	if '1' not in gig_types:
		gig_terms.full_time = False
	if '2' not in gig_types:
		gig_terms.contract = False
	if '3' not in gig_types:
		gig_terms.freelance = False
	if '4' not in gig_types:
		gig_terms.internship = False

	gig_terms.save()
	


def get_results(what, location, page, gig_types):
	terms = _prepare_words(what)
	#results = Gig.objects.all()
	results = []
	
	try:
		page = int(page)
		if page == 1:
			start = 0
			end = settings.GIGS_PER_PAGE
		else :
			end = page * settings.GIGS_PER_PAGE
			start = end - settings.GIGS_PER_PAGE
	except:
		pass
	#| Q(tags__icontains = what )
	gigs = Gig.objects.filter(site_id=current_site_id())\
			.filter(Q(title__icontains = what)|Q(description__icontains = what)| Q(company__company_name__icontains = what )
				)\
			.filter(site_id=current_site_id()).filter(Q(location__icontains = location) | Q(area_level2__icontains = location)).order_by('-publish_date')[start:end]

	gig_types_list = gig_types.split()
	# Any remote jobs
	if '0' in gig_types_list:
		print 'remote'
		gigs = gigs.filter(is_remote = True) # Remote gigs
		gig_types_list.pop(gig_types_list.index('0'))

	# Exclude all unchecked gig types
	for gig_type in gig_types_list:
		gigs = gigs.exclude(job_type = GigType.objects.get(pk = gig_type))

	for gig in gigs:
		results.append({
			'gig_id' : gig.id,
			'gig_title' : gig.title,
			'gig_link' : gig.get_absolute_url(),
			'gig_job_type' : gig.job_type.type,
			'gig_publish_date' : date(gig.publish_date),
			'gig_company' : gig.company.company_name,
			'gig_company_elevator_pitch' : gig.company.elevator_pitch,
			'gig_company_logo' : gig.company.profile_picture.name\
				 if gig.company.profile_picture.name else 'company_logos/employer_default.png',
			'gig_company_profile' : reverse('company_profile', args = (gig.company.slug,)),
			'gig_location' : gig.location,
			'gig_is_new' : 'today' in naturalday(gig.publish_date),
			'gig_tags' : gig.get_tags() if gig.hidden_tags else False,
		})
	# the results are either resumes or gigs or a company
	return results

def _prepare_words(what):
	"""
	Filter search query from common words like 'a, the, etc'
	based on the site language
	"""
	# Should implement filter based on common words based on 
	# site language
	if what:
		query_terms = what.split()
		search_terms = [ term for term in query_terms if term not in STRIP_WORDS]
		return search_terms[0:5]
