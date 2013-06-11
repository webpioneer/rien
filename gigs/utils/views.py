from django.http import HttpResponse
from django.utils import simplejson

from cartridge.shop.models import ProductVariation
from mezzanine.utils.timezone import now

from gigs.models import Application

def application_messages(application, user = None, application_followup = []):
    
    for message in application.next_messages.all().order_by('sent_at'):
        if user == message.recipient and message.read_at is None:
            message.read_at = now()
            message.save()
        application_followup.append(message)
        application_messages(message, user , application_followup)
    return application_followup

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


def application_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Application.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True).count()


def unread_applications(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen
    """
    return Application.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True)

