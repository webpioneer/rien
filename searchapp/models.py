from django.contrib.auth.models import User
from django.db import models

from mezzanine.core.models import Displayable

from gigs.models import GigType


class BaseSearch(Displayable):
	"""
	Base Model for Search
	"""
	what = models.CharField(max_length = 100, null = True, blank = True)
	location = models.CharField(max_length = 50, null = True, blank = True)
	longitude = models.CharField(max_length = 25, null = True, blank = True)
	latitude = models.CharField(max_length = 25, null = True, blank = True)
	area_level1 = models.CharField(max_length = 20, blank = True, null = True)
	area_level2 = models.CharField(max_length = 20, blank = True, null = True)
	ip_address = models.GenericIPAddressField()
	user = models.ForeignKey(User, null = True, blank = True)
	subscribed_user = models.EmailField(blank = True, null = True)

	class Meta:
		abstract = True

class ResumeSearch(BaseSearch):
	pass

class GigSearch(BaseSearch):
	is_onsite = models.NullBooleanField()
	gig_type = models.ManyToManyField(GigType)
	#full_time = models.NullBooleanField(default=True)
	#contract = models.NullBooleanField(default=True)
	#freelance = models.NullBooleanField(default=True)
	#internship = models.NullBooleanField(default=True)

	def __unicode__(self):
		return ("{0} {1}").format(self.what, self.location)

    
