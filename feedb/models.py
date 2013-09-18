from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.models import Ownable
from mezzanine.utils import timezone


class FeedbackBase(models.Model):
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	site = models.ForeignKey(Site)

	class Meta:
		abstract = True


RATING_RANGE = [ i/2.0 for i in range(settings.RATINGS_MIN, ((settings.RATINGS_MAX + 1) * 2) - 1)]


class Feedback(Ownable, FeedbackBase):
	feedback = models.TextField(_('Feedback'))
	rating = models.FloatField(_("Rating"), blank = True, null = True)

	# Metadata about the Feedback
	submit_date = models.DateTimeField(_('date/time submitted'), default=None)

	def __unicode__(self):
		return '%s (%s) by %s to %s(%s)' % (self.feedback, self.rating, self.user,
		 self.content_object.__class__.__name__, self.content_object.id)

	def save(self, *args, **kwargs):
		if self.submit_date is None:
			self.submit_date = timezone.now()
		if self.rating not in RATING_RANGE:
			raise ValueError("Invalid rating. %s is not within %s and %s" %
                             (self.rating, RATING_RANGE[0], RATING_RANGE[-1]))

		super(FeedbackBase, self).save(*args, **kwargs)