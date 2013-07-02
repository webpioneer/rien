from django.db.models import get_models, signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    @receiver(post_save, sender = User, dispatch_uid="my_unique_identifier")
	def set_user_default_settings(sender, **kwargs):
    	print kwargs
    	for notice_type in notification.NoticeType.objects.filter(label__startswith = 'messages'):
        	print notice_type
        	try:
            	notification.NoticeSetting(user = kwargs['instance'], 
                notice_type = notice_type, medium = '0', send = True).save()
        	except:
            	pass
