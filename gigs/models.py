from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Slugged, Displayable
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to

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

class Company(Displayable):
    """
    Company Model
    """
    COMPANY_TYPES = (
        ('STARTUP', "Startup"),
        ('STUDIO', "Studio"),
        ('SMALL_BUSINESS', "Small Business"),
        ('MID_SIZED_BUSINESS', "Mid Sized Business"),
        ('LARGE_ORGANIZATION', "Large Organization"),
        ('EDUCATIONAL_INSTITUTION', "Educational Institution"),
        ('NON_PROFIT', "Non-profit"),
    )
    type = models.CharField(max_length = 200, choices = COMPANY_TYPES)
    title_is_confidential = models.BooleanField(default = False,
                    verbose_name = _("Confidential"))
    url = models.URLField(verbose_name = _("Company URL"))
    elevator_pitch = models.TextField(verbose_name = _("Elevator pitch"))
    # figure out upload_to function and its 2 arguments
    profile_picture = FileField(verbose_name = _('Profile Picture'),
        upload_to = 'company_logos', format = 'Image',
        max_length=255, null=True, blank=True)                        
    ip_address = models.GenericIPAddressField()

    class Meta:
        verbose_name_plural = _("Companies")

class Gig(models.Model):
    pass
