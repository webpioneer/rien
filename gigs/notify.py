from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.utils.email import send_mail_template

from gigs.models import Company

@receiver(post_save, sender = Company)
def welcome_company(sender, **kwargs):
    print kwargs
    subject = 'welcome'
    addr_from = 'elmahdibouhram@els-MacBook-Pro.local'
    #addr_to = sender.email
    addr_to = 'elmahdibouhram@els-MacBook-Pro.local'
    template = "email/comment_notification"
    send_mail_template(subject, template, addr_from, addr_to, context=None,
                       attachments=None, fail_silently = settings.DEBUG)