import moneyed

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import settings

from cartridge.shop.models import Product

from mezzanine.core.models import Slugged, Displayable, RichText
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.utils.models import upload_to

from djmoney.models.fields import MoneyField



class Category(Slugged):
    """
    Job Category
    """
    pub_date = models.DateTimeField(auto_now_add = True)
    is_custom = models.BooleanField()

    class Meta:
        verbose_name = _("Job Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return ("%s") % (self.title)
    
    @models.permalink
    def get_absolute_url(self):
        return ('gigs_list_category',(),{'slug':self.slug})


COMPANY_LOGO_DEFAULT = getattr(settings, 'COMPANY_LOGO_DEFAULT', 'static/media/company_logos/employer_default.png')

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
    PROFILE_PICTURE_SOURCE = (
        ('NO_PICTURE', _('No picture')),
        ('TWITTER_PICTURE', _('Use Twitter profile picture (recommended)')),
        ('OWN_PICTURE', _('Upload a picture')),
    )
    company_name = models.CharField(_('Company name'), max_length = 500)
    type = models.CharField(max_length = 200, choices = COMPANY_TYPES,
                    verbose_name = _('Company type'))
    title_is_confidential = models.BooleanField(verbose_name = _("Confidential"))
    url = models.URLField(verbose_name = _("Company URL"))
    email = models.EmailField()
    elevator_pitch = models.CharField(max_length = 200, verbose_name = _("Elevator pitch"),
        help_text=_("What s your company about (i.e. tag line)"))
    # figure out upload_to function and its 2 arguments
    profile_picture_choice = models.CharField(max_length = 60, 
        choices = PROFILE_PICTURE_SOURCE, default = PROFILE_PICTURE_SOURCE[0][1])
    #profile_picture = FileField(verbose_name = _('Profile Picture'),
    #    upload_to = 'company_logos', format = 'Image',
    #    max_length=255, null=True, blank=True)   
    profile_picture = models.ImageField(verbose_name= _('Profile Picture'),
        upload_to = 'company_logos', max_length=255,
        null = True, blank = True, default = COMPANY_LOGO_DEFAULT)                     
    ip_address = models.GenericIPAddressField()
    user = models.OneToOneField(User) 

    class Meta:
        verbose_name_plural = _("Companies")

    def save(self, *args, **kwargs):
        company_password = User.objects.make_random_password()
        print company_password
        self.user = User.objects.create_user(username = self.email, email = self.email,
         password = company_password)
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return ("{0} {1} {2}").format(self.title, self.type, self.profile_picture)

class GigType(models.Model):
    """
    Gig Type 
    """
    type = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')

    def __unicode__(self):
        return ("%s %s") % (self.type, self.price)

class Gig(Product):
    """
    Gig Model
    Gig(job_type, location, latitude, longitude, is_relocation, is_onsite, descr,
        perks, how_to_apply, via_email, via_url. apply_instructions, is_filled,
        categories, company)
    """
    HOW_TO_APPLY_CHOICES = (
        ('VIA_EMAIL','by Email'),
        ('VIA_URL', 'via URL'),
    )
    job_type = models.ForeignKey('GigType', verbose_name = _('Job Type'))
    location = models.CharField(max_length = 200, verbose_name = _('Job Location'),
        help_text=_("Examples: San Francisco, CA; Seattle; Anywhere"))
    latitude = models.CharField(max_length = 25)
    longitude = models.CharField(max_length = 25)
    is_relocation = models.BooleanField(verbose_name = _("Relocation assistance offered\
                for this opposition"))
    is_onsite = models.BooleanField(verbose_name = _("Work can be done from anywhere \
        (i.e. telecommuting)"))
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
    is_filled = models.BooleanField(verbose_name = _("Filled"))
    gig_categories = models.ManyToManyField('Category')
    company = models.ForeignKey('Company')
    product = models.OneToOneField(Product)
    
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
