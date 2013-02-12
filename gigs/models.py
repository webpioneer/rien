import moneyed

from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Slugged, Displayable, RichText
from mezzanine.core.fields import FileField
from mezzanine.utils.models import upload_to

from djmoney.models.fields import MoneyField

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

class GigType(models.Model):
    """
    Gig Type 
    """
    type = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
   
    def __unicode__(self):
        return self.type, self.price

class Gig(Displayable, RichText):
    """
    Gig Model
    """
    type = models.ForeignKey('GigType')
    location = models.CharField(max_length = 200, verbose_name = _('Job Location'),
        help_text=_("Examples: San Francisco, CA; Seattle; Anywhere"))
    latitude = models.CharField(max_length = 15)
    longitude = models.CharField(max_length = 15)
    is_relocation = models.BooleanField(verbose_name = _("Relocation assistance offered\
                for this opposition"),default = False)
    is_onsite = models.BooleanField(verbose_name = _("Work can be done from anywhere \
        (i.e. telecommuting)"), default = False)
    perks = models.TextField(verbose_name = _("Job Perks"), 
    help_text = _("Sell your position! If you're willing to relocate, mention \
    it here. If you've got great benefits, bonuses, paid trips to conferences, \
    free food, discounts, etc., talk it up."))
    is_filled = models.BooleanField(verbose_name = _("Filled"), default = False)
    categories = models.ManyToManyField('Category')
    company = models.ForeignKey('Company')

    class Meta:
        verbose_name = "Gig"
        verbose_name_plural = "Jobs"


class GigStat(models.Model):
    """ 
    Stats about a given Gig
    """
    views = models.IntegerField(verbose_name = _("Number of Views"))
    clicked_apply = models.IntegerField(verbose_name = _("Clicked Apply"))
    notified_users = models.IntegerField(verbose_name = _("Notified Users"))

    class Meta:
        verbose_name = 'Job Stats'
