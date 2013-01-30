from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Slugged

class Category(Slugged):
    """
    Job Category
    """
    pub_date = models.DateTimeField(auto_now_add = True)
    is_custom = models.BooleanField(default = False)

    class Meta:
        verbose_name = _("Job Category")
        verbose_name_plural = _("Categories")
    
    @models.permalink
    def get_absolute_url(self):
        return ('gigs_list_category',(),{'slug':self.slug})
