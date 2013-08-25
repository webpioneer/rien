import moneyed

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
import settings

from cartridge.shop.models import Product, OrderItem

from mezzanine.core.models import Slugged, Displayable, RichText
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.utils.models import upload_to
from mezzanine.utils.timezone import now

from django_messages.models import Message
from djmoney.models.fields import MoneyField

def get_app_mother(message):
    """ returns the mother app if any """
    print message.id, message.body
    if message.parent_msg == None:
        print message.id, message.body
        return message
    get_app_mother(message.parent_msg)

class Resume(models.Model):
    file = models.FileField(upload_to = 'resumes')
    user = models.ForeignKey(User)
    created_at = now()
    is_enabled = models.BooleanField(default = True)

    def __unicode__(self):
        return ('{0} {1} {2}').format(self.file, self.user, self.created_at)

    def get_filename(self):
        return self.file.file.name.split('/')[-1].capitalize()

class Application(Message):
    """Reprsents an application from an applier regarding a gig """
    #message = models.OneToOneField(Message)
    gig = models.ForeignKey('Gig', null = True, blank = True)
    favorited_at = models.DateTimeField(null = True, blank = True)
    rejected_at = models.DateTimeField(null = True, blank = True)
    printed_at = models.DateTimeField(null = True, blank = True)
    resume = models.ForeignKey(Resume)

    def __unicode__(self):
        return "{0} {1} {2}".format(self.sender, self.recipient, self.resume)

    @models.permalink
    def get_absolute_url(self):
        url_name = 'application_detail'
        #mother_app = get_app_mother(self)
        #print mother_app
        kwargs = {"message_id" : self.id}
        return (url_name, (), kwargs)

    def is_application(self):
        if self.__class__.__name__ == 'Application':
            return True

    def get_mother_app(self, **kwargs):
        if self.parent_msg is None:
            return self
        self.get_mother_app(**kwargs)

    @property
    def get_resume(self):
        return self.resume.file

    @property
    def get_resume_name(self):
        return self.resume.file.name.split('/')[1]



def inbox_count_for(user):
    """
    returns the number of unread messages for the given user but does not
    mark them seen and the message IS NOT an application
    """
    return Message.objects.filter(recipient=user, read_at__isnull=True, recipient_deleted_at__isnull=True, application__isnull=True).count()


class Category(Slugged):
    """
    Job Category
    """
    pub_date = models.DateTimeField(auto_now_add = True)
    description = models.CharField(max_length = 50, null = True, blank = True)
    is_custom = models.BooleanField()

    class Meta:
        verbose_name = _("Job Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return ("%s") % (self.title)
    
    @models.permalink
    def get_absolute_url(self):
        return ('gigs_list_category',(),{'slug':self.slug})


COMPANY_LOGO_DEFAULT = getattr(settings, 'COMPANY_LOGO_DEFAULT', 'static/media/company_logos/.thumbnails/employer_default.png')
APPLIER_PICTURE_DEFAULT = getattr(settings, 'APPLIER_PICTURE_DEFAULT', 'static/media/company_logos/.thumbnails/employer_default.png')

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
    url = models.URLField(verbose_name = _("Company URL"), null = True, blank = True)
    email = models.EmailField()
    elevator_pitch = models.CharField(max_length = 200, verbose_name = _("Elevator pitch"),
        help_text=_("What s your company about (i.e. tag line)"))
    # figure out upload_to function and its 2 arguments
    profile_picture_choice = models.CharField(max_length = 60, 
        choices = PROFILE_PICTURE_SOURCE, default = PROFILE_PICTURE_SOURCE[0][1])  
    profile_picture = models.ImageField(verbose_name= _('Profile Picture'),
        upload_to = 'company_logos', max_length=255,
        null = True, blank = True, default = COMPANY_LOGO_DEFAULT)
    twitter_username = models.CharField(max_length = 50, null= True, blank = True)                      
    ip_address = models.GenericIPAddressField()
    user = models.OneToOneField(User) 

    class Meta:
        verbose_name_plural = _("Companies")

    def save(self, *args, **kwargs):
        if 'force_update' in kwargs.keys():
            print 'update force %s ' % kwargs['force_update']
        company_password = User.objects.make_random_password()
        print 'company password : %s' % company_password
        if 'force_update' not in kwargs.keys():
                        #User.objects.get_or_create(username = self.email, email = self.email,
                        # password = company_password)
            #self.user = User.objects.get_or_create(username = self.email, email = self.email,
            #             password = company_password)
            
            self.user = User.objects.create_user(username = self.email, email = self.email,
                         password = company_password)
        super(Company, self).save(*args, **kwargs)
        
        return company_password


    def __unicode__(self):
        return ("{0} {1} {2} {3} {4}").format(self.company_name, self.email, self.url,  self.type, self.profile_picture)

    def number_posted_gigs(self):
        return self.gig_set.count()

    def company_gigs(self):
        return self.gig_set.all().order_by('-publish_date')

    def gigs(self):
        return self.gig_set.all()

class Applier(Displayable):
    # title
    PROFILE_PICTURE_SOURCE = (
        ('NO_PICTURE', _('No picture')),
        ('TWITTER_PICTURE', _('Use Twitter profile picture (recommended)')),
        ('OWN_PICTURE', _('Upload a picture')),
    )

    profile_picture_choice = models.CharField(max_length = 60, 
        choices = PROFILE_PICTURE_SOURCE, default = PROFILE_PICTURE_SOURCE[0][1])
    profile_picture = models.ImageField(verbose_name= _('Profile Picture'),
        upload_to = 'applier_pictures', max_length=255,
        null = True, blank = True, default = APPLIER_PICTURE_DEFAULT)
    twitter_username = models.CharField(max_length = 50, null= True, blank = True)                      
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length = 200, null = True, blank = True,
        verbose_name = _('Job Location'),
        help_text=_("Examples: San Francisco, CA; Seattle; Anywhere"))
    latitude = models.CharField(max_length = 25, null = True, blank = True)
    longitude = models.CharField(max_length = 25, null = True, blank = True)
    area_level1 = models.CharField(max_length = 20, blank = True, null = True)
    area_level2 = models.CharField(max_length = 20, blank = True, null = True)
    # resume : an applier can have one or more resumes
    #resume = models.FileField(verbose_name=_("Resume"), blank=True,
    #    upload_to=upload_to("gigs.Applier.resume", "resumes"), help_text=_("Upload your resume"))
    is_relocation = models.NullBooleanField(verbose_name = _("Ready to relocate"), null = True, blank = True, default = True)
    is_looking = models.NullBooleanField(null = True, blank = True, default = True)
    #phone_number refers to https://github.com/daviddrysdale/python-phonenumbers
    #about_me = description
    # experience, education many to many field
    # social networks Foreign Key
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.username, self.email, self.location

class GigType(Slugged):
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
    area_level1 = models.CharField(max_length = 25, blank = True, null = True)
    area_level2 = models.CharField(max_length = 25, blank = True, null = True)
    area_level3 = models.CharField(max_length = 25, blank = True, null = True)
    area_level4 = models.CharField(max_length = 25, blank = True, null = True)
    is_relocation = models.BooleanField(verbose_name = _("Relocation assistance offered\
                for this opposition"))
    is_remote = models.BooleanField(verbose_name = _("Work can be done from anywhere \
        (i.e. telecommuting)"))
    perks = models.TextField(verbose_name = _("Job Perks"), blank = True, 
        null = True, help_text = _("Sell your position! If you're willing \
        to relocate, mention it here. If you've got great benefits, bonuses\
        , paid trips to conferences, free food, discounts, etc., talk it up."))
    how_to_apply = models.CharField(max_length = 15, choices = HOW_TO_APPLY_CHOICES,
                    default = HOW_TO_APPLY_CHOICES[0][0], verbose_name = _('How to apply'))
    tags = models.CharField(max_length = 100, null = True, blank = True)
    hidden_tags = models.CharField(max_length = 100, null = True, blank = True)
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

    @models.permalink
    def get_absolute_url(self):
        url_name = 'get_gig'
        kwargs = {"slug" : self.slug}
        return (url_name, (), kwargs)

    def is_processed(self):
        try:
            status = True if OrderItem.objects.filter(sku = self.product.variations.all()[0].sku)[0].order.status == 2 else False
            return status
        except IndexError:
            return False

    def applications(self):
        return self.application_set.filter(gig__isnull= False)

    def num_applications(self):
        return self.application_set.count()

    def get_tags(self):
        return self.hidden_tags.split(',') if self.hidden_tags else False

class GigStat(models.Model):
    """ 
    Stats about a given Gig
    """
    views = models.IntegerField(verbose_name = _("Number of Views"))
    clicked_apply = models.IntegerField(verbose_name = _("Clicked Apply"))
    notified_users = models.IntegerField(verbose_name = _("Notified Users"))

    class Meta:
        verbose_name = 'Job Stats'
