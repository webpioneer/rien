from django.http import HttpResponse
from django.utils import simplejson

from cartridge.shop.models import ProductVariation

def get_gig_info(request, sku):
	"""
	Returns gig object from sku
	"""
	gig = ProductVariation.objects.filter(sku = sku)[0].product.gig
	response = simplejson.dumps({
				'gig_type' : gig.job_type.type,
				'gig_picture' : gig.company.twitter_username or gig.company.profile_picture.name,
				'gig_twitter_username' : gig.company.twitter_username,
				})
	return HttpResponse(response, content_type='application/javascript')
