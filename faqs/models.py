from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Displayable, Orderable, RichText, Slugged

#from faqs.managers import FaqManager

#class FaqCategory(Orderable, Slugged):
#	pass

class Faq(Orderable, Displayable, RichText):
	"""
	Frequently Asked Question
	Note : i put Orderable first, then it works
	"""
	#categories = models.ManyToManyField(FaqCategory)

	#objects = FaqManager()
	pass

	def __unicode__(self):
		return u'Q : {0} - A : {1}'.format(self.title, self.content)

