import moneyed

from django.contrib.auth.models import User
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

    def __unicode__(self):
        return ("%s %s") % (self.title, self.is_custom)
    
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
    email = models.EmailField()
    elevator_pitch = models.TextField(verbose_name = _("Elevator pitch"))
    # figure out upload_to function and its 2 arguments
    profile_picture = FileField(verbose_name = _('Profile Picture'),
        upload_to = 'company_logos', format = 'Image',
        max_length=255, null=True, blank=True)                        
    ip_address = models.GenericIPAddressField()
    user = models.OneToOneField(User) 

    class Meta:
        verbose_name_plural = _("Companies")

    def save(self, *args, **kwargs):
        company_password = User.objects.make_random_password()
        self.user = User.objects.create_user(username = self.title, email = self.email, password = company_password)
        super(Company, self).save(*args, **kwargs)

class GigType(models.Model):
    """
    Gig Type 
    """
    type = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
   
    def __unicode__(self):
        return ("%s %s") % (self.type, self.price)

class Gig(Displayable, RichText):
    """
    Gig Model
    """
    HOW_TO_APPLY_CHOICES = (
        ('VIA_EMAIL','by Email'),
        ('VIA_URL', 'via URL'),
    )
    type = models.ForeignKey('GigType', verbose_name = _('Job Type'))
    location = models.CharField(max_length = 200, verbose_name = _('Job Location'),
        help_text=_("Examples: San Francisco, CA; Seattle; Anywhere"))
    latitude = models.CharField(max_length = 15)
    longitude = models.CharField(max_length = 15)
    is_relocation = models.BooleanField(verbose_name = _("Relocation assistance offered\
                for this opposition"),default = False)
    is_onsite = models.BooleanField(verbose_name = _("Work can be done from anywhere \
        (i.e. telecommuting)"), default = False)
    perks = models.TextField(verbose_name = _("Job Perks"), blank = True, 
        null = True, help_text = _("Sell your position! If you're willing \
        to relocate, mention it here. If you've got great benefits, bonuses\
        , paid trips to conferences, free food, discounts, etc., talk it up."))
    how_to_apply = models.CharField(max_length = 15, choices = HOW_TO_APPLY_CHOICES,
                    default = HOW_TO_APPLY_CHOICES[0][0], verbose_name = _('How to apply'))
    via_email = models.EmailField(blank = True, null = True)
    via_url = models.URLField(blank = True, null = True)
    apply_instructions = models.TextField(null = True, blank = True,
            verbose_name = _('Add instructions(optional)'))
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
