from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
# find a use for reverse
#from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.sites import current_site_id
from mezzanine.conf import settings

from gigs.models import Gig, GigType
from searchapp.search import get_results

class GigFeed(Feed):
	"""
	RSS Feed for gigs
	"""

	# need to add Description

	def get_object(self, request, *args, **kwargs):
		self.what = request.GET.get('what', None)
		self.location = request.GET.get('location', None)
		gig_types = GigType.objects.all()
		if request.GET.get('gig_types_string'):
			self.gig_types_list = [ gig_type.id for gig_type in gig_types 
				if str(gig_type.id) not in request.GET.get('gig_types_string')]
		else:
			self.gig_types_list = list()
		self.remote = request.GET.get('remote', False)

	def link(self):
		# need to not hard code it
		return '/jobs/feed/'

	def title(self):
		settings.use_editable()
		return _('%s Job Listings' %  settings.SITE_TITLE)
	
	def items(self):
		
		return get_results(what = self.what, location = self.location,
		 page = 1, gig_types_list = self.gig_types_list, remote = self.remote)

	def item_title(self, item):
		return '[%s] %s, %s' % (item.job_type.type, item.title.capitalize(), item.location)


	def item_description(self, item):
		# would i just want to return 25 words or the whole descr
		return truncate_words(item.description.capitalize(), num = 25)

	def item_pubdate(self, item):
		return item.publish_date

	def item_categories(self, item):
		return [ category for category in item.gig_categories.all()]
