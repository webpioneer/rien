from gigs.models import inbox_count_for
from gigs.utils.views import application_count_for, unread_applications

def inbox(request):
    if request.user.is_authenticated():
        return {
        	'messages_inbox_count': inbox_count_for(request.user),
        	'applications_inbox_count' : application_count_for(request.user),
        	'unread_applications' : unread_applications(request.user),
        }
    else:
        return {}
