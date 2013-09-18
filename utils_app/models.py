from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Ownable

from gigs.models import Application

class EmailContentBase(models.Model):
	recipients = models.CharField(max_length = 1000)
	subject = models.CharField(max_length=300, default = _('Resume Forwarded from {0}'.format('hello')))
	body = models.TextField()
	sender = models.ForeignKey(User)

	def __unicode__(self):
		return '{0} sent {1} to {2}'.format(self.sender,
		 self.subject, self.recipients)

class EmailedResume(EmailContentBase):
	
	application = models.ForeignKey(Application)

	def __unicode__(self):
		return '{0} sent {1} to {2}'.format(self.sender, 
			self.application, self.recipients)

class Team(Ownable, Group):
	#pass
	def __unicode__(self):
		return self.name


class GroupWithType(Group, Ownable):
	"""
	Group model with a type attribute
	A company owns a group (Intwerviewer, Recruiter) and 1 or more
	users belong to this group owned by the company
	"""
	TYPE_CHOICES = (
		('INTERVIEWER', _('Interviewer')),
		('RECRUITER', _('Recruiter')),
		#('ADMIN', _('Administrator')),
		)
	group_type = models.CharField(max_length = 15, choices = TYPE_CHOICES,
		default = TYPE_CHOICES[0][0])

	def __unicode__(self):
		return '%s(%s) owner by %s' % (self.name, self.group_type, self.user)


