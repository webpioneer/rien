from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.messages import info
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db.models import Min
from django.dispatch import receiver
from django.shortcuts import HttpResponse, get_object_or_404, render_to_response, redirect
from django.template import Context, RequestContext, loader
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required




from cartridge.shop.forms import AddProductForm
from cartridge.shop.models import (Cart, CartItem, Product,
 ProductImage, ProductVariation)
from cartridge.shop.views import cart, product as product_view

from mezzanine.accounts import get_profile_form
from mezzanine.conf import settings
from mezzanine.utils.views import paginate, render
from mezzanine.utils.sites import current_site_id
from mezzanine.utils.timezone import now
from mezzanine.utils.urls import slugify

from django_messages.models import Message
from notification.models import NoticeSetting


from gigs.forms import CompanyForm, PostJobForm, ApplyForm, ReplyForm, ProfileForm2
from gigs.models import Category, Gig, GigType, Application, Resume
from gigs.signals import user_added_to_group
from gigs.utils.views import application_messages
from searchapp.forms import GigSearchForm

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification
else:
    notification = None


def all_gigs(request, template_name = 'gigs/index.html'):
    """
    Returns gigs on the home page
    """
    # gigs need to be filtred based on order processed
    # based on site_id,etc by creating a models.Manager

    settings.use_editable()
    site_id = current_site_id()
    gigs = Gig.objects.all().filter(site_id = site_id).order_by('-publish_date')[0:5]
    categories = Category.objects.all().filter(site_id = site_id)
    #starting_price = GigType.get_starting_price()
    starting_price = GigType.objects.all().aggregate(Min('price'))['price__min']
    # for search and filtering
    gig_types = GigType.objects.all()
    # search form
    gig_search_form = GigSearchForm()
    context = {
        'gigs' : gigs,
        'categories' : categories,
        'gig_types' : gig_types,
        'starting_price' : starting_price,
        'gig_search_form' : gig_search_form,
    }
    return render(request, template_name, context)

def get_gig(request, slug = None,template_name = 'gigs/get_gig.html'):
    """
    Returns the Gig page
    """   
    try:
        gig = get_object_or_404(Gig, slug = slug)
        apply_form = ApplyForm()
        signup_form = ProfileForm2()

        if 'shop/product' in request.META['HTTP_REFERER']:
            message = _('Your listing is published successfully. \
            Please visit "%s" to track listing statistics, make edits, and more.') % gig.company.email
            info(request, message)
    except:
        pass
        
    context = {
        'gig' : gig,
        'apply_form' : apply_form,
        'signup_form' : signup_form,
    }   
    return render(request, template_name, context)

def post_job(request, template_name = 'gigs/post_job.html'):
    """ 
    Post Job Form 
    """
    gig_types = GigType.objects.all()
    if request.method == 'POST':
        post_job_form = PostJobForm(request.POST)
        company_form = CompanyForm(request.POST, request.FILES)
        #post_job_form_data = post_job_form.get_gig_create_data()

        if  post_job_form.is_valid():
            print 'forms are valid'
            # save company first
            if request.user.is_authenticated() and request.user.company:
                company = request.user.company
            else:
                if company_form.is_valid():
                    company = company_form.get_company_object()
                    company.slug = slugify(company.company_name)
                    print company.slug
                    company.ip_address = request.META['REMOTE_ADDR']
                    #company.profile_picture = company_form.cleaned_data['profile_picture']
                    #company.profile_picture = request.FILES.get('profile_picture', '')
                    company_password = company.save()
                    # Add company to the group Company
                    company_group = Group.objects.get(name = 'Company')
                    company.user.groups.add(company_group)
                    # send a signal that a user is added to a group
                    user_added_to_group.send(sender = post_job.func_name,
                        user = company.user, group = 'Company')
                    # authenticate company
                    print company.user.username
                    print company.user.password
                    user = authenticate(username=company.user.username, password=company_password)
                    print user
                    login(request, user)
            # save gig
            gig = post_job_form.get_gig_object()
            gig.company = company
            # categories
            gig_categories = post_job_form.cleaned_data['gig_categories']
            #print request.FILES['profile_picture']
            if 'Preview your listing' == request.POST['submit']:
                # call view preview listing
                print 'preview'
                request.session['company'] = company
                request.session['gig'] = gig
                request.session['gig_categories'] = gig_categories
                gig.available = True
                gig.unit_price = 100

                gig.image = company.profile_picture
                # updating the status to draft (needs review)
                # gig.status = 1
                gig.save()
                
                gig_variation = ProductVariation(product = gig, default = True,
                 unit_price = gig.job_type.price.amount, sale_price = gig.job_type.price.amount)
                gig_variation.save()
                print 'product variation sku %s'  % gig_variation.sku
                product_image = ProductImage(file = company.profile_picture, product = gig)
                product_image.save()
                for category in gig_categories:
                    gig.gig_categories.add(category)
                
                return redirect("shop_product", slug = gig.slug)
                #template = 'gigs/gig_product.html'
                #product_view(slug = gig.slug, template = template)
    else:
        post_job_form = PostJobForm()
        company_form = CompanyForm()
    context = {
        'gig_categories' : Category.objects.all(),
        'post_job_form': post_job_form, 'company_form': company_form,
        'gig_types': gig_types,
        'title': _('Create Your Job Listing'),
        'company_information': _('Company Information'),
        }
    return render(request, template_name, context)


from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.utils.email import send_mail_template

from gigs.models import Company

@receiver(post_save, sender = Company)
def welcome_company(sender, **kwargs):
    print kwargs
    subject = 'welcome'
    addr_from = 'elmahdibouhram@els-MacBook-Pro.local'
    #addr_to = sender.email
    addr_to = 'elmahdibouhram@els-MacBook-Pro.local'
    template = "email/comment_notification"
    send_mail_template(subject, template, addr_from, addr_to, context=None,
                       attachments=None, fail_silently = settings.DEBUG)

def gig_product(request, slug, template_name = 'gigs/gig_product.html'):
    product = request.session['product']
    variations = product.variations.all()
    initial = {}

    add_product_form = AddProductForm(request.POST, product=product, to_cart = True)
    if request.method == "POST":
        if add_product_form.is_valid():
            quantity = add_product_form.cleaned_data["quantity"]
            request.cart.add_item(add_product_form.variation, quantity)
            info(request, _("Item added to cart"))
            return redirect("shop_cart")
    context ={
        'gig' : request.session['gig'],
        'product' : product,
        'variations' : variations,
        'add_product_form' : add_product_form,
    }
    return render(request, template_name, context)

@login_required
def company_listings(request, template_name = 'gigs/company/company_listings.html'):
    """ returns a list of gigs based on the logged in company """
    context = {}
    return render(request, template_name, context)

@login_required
def company_infos(request, template_name ='gigs/company/company_infos.html'):
    """ handle the input of the company Information """
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            company = company_form.get_company_object()
            company.save()

    else:
        company_form = CompanyForm(instance = request.user.company)
    context = {
        'company_form' : company_form,
    }
    return render(request, template_name, context)

def company_profile(request, slug, template_name = 'gigs/company/company_profile.html'):
    """ returns the public company profile """
    company = get_object_or_404(Company, slug = slug)
    context = {'company' : company,
                'hey' : True }
    return render(request, template_name, context)

def view_listing(request, slug, template_name = 'gigs/company/view_listing.html'):

    gig = get_object_or_404(Gig, slug = slug)
    context = {
        'gig' : gig,
    }
    return render(request, template_name, context)



#Applier 

@login_required
def applier_applications(request, template_name = 'gigs/applier/applier_applications.html'):
    """ returns a list of applications related to an applier """
    applications = Application.objects.filter(sender = request.user).filter(gig__isnull = False)
    context = {
        'applications' : applications,
    }
    return render(request, template_name, context)

def apply(request, gig_slug, template_name = 'gigs/apply.html'):
    """ handle applying to an application """
    gig = get_object_or_404(Gig, slug = gig_slug)

    if request.method == 'POST':
        signup_form = ProfileForm2(request.POST)
        apply_form = ApplyForm(request.POST, request.FILES)

        if request.user.is_authenticated():
            #if apply_form.is_valid():
                user = request.user
                #apply_form.save()
                application = Application()
                application.subject = gig.title
                application.sender = user
                application.recipient = gig.company.user
                application.gig = gig
                if not apply_form.fields['motivation'].clean(request.POST.get('motivation')):
                    return redirect(gig.get_absolute_url())
                application.body = request.POST.get('motivation')
                print 'select_resume: %s'  % request.POST.get('select_resume')
                print request.FILES.get('resume')

                # upload file
                if request.FILES.get('resume'):
                    print 'resume'
                    if not apply_form.fields['resume']:
                        apply_form.clean_resume()
                        return redirect(gig.get_absolute_url())
                    resume = Resume(file = request.FILES['resume'], user = user)
                    resume.save()
                    application.resume = resume
                else:
                    resume_id = request.POST.get('select_resume')
                    resume = Resume.objects.get( pk = resume_id)
                    print resume
                    print 'here %s' % resume
                    application.resume = resume
                
                application.save()
                print application
                message = _('You applied successfully')
                info(request, message, extra_tags='success')
                if notification:
                    notification.send([application.recipient], "applications_received", {'message': message,})

                return redirect(gig.get_absolute_url())
        else:
            if signup_form.is_valid() and apply_form.is_valid():
                print 'both forms are valid'
                user, password = signup_form.save()
                # send signal user_added_to_group
                user_added_to_group.send(sender = apply.func_name,
                        user = user, group = 'JobSeeker')
                
                application = Application()
                application.subject = gig.title
                application.sender = user
                application.recipient = gig.company.user
                application.gig = gig
                application.body = apply_form.cleaned_data['motivation']
                # upload file
                resume = Resume(file = request.FILES['resume'], user = user)
                resume.save()
                application.resume = resume
                application.save()
                
                user = authenticate(username = user.username,
                                    password = password)
                login(request, user)
                message = _('You applied successfully')
                # an email is sent to the user with his new password
                info(request, message, extra_tags='success')
                if notification:
                    notification.send([user], "applications_received", {'message': message,})
                
                return redirect(gig.get_absolute_url())
    else:
        signup_form = ProfileForm2()
        apply_form = ApplyForm()

    context = {
        'signup_form' : signup_form,
        'apply_form': apply_form,
        'gig' : gig,
    }
    return render(request, template_name, context)

def reply_to_apply(request, application_id, template_name = 'gigs/applier/application_detail.html'):
    """ handles reply to application """
    print 'CALL TO : reply_to_apply - > %s' % application_id
    app = get_object_or_404(Application, id = application_id)
    if request.method == 'POST':
        reply_form = ReplyForm(request.POST)
        print reply_form
        if reply_form.is_valid():
            print 'reply form is valid'
            application = Application()
            #application.subject = gig.title
            application.sender = request.user
            application.recipient = app.sender
            application.body = reply_form.cleaned_data['reply']
            application.parent_msg = app
            application.save()
            print application.sender, application.recipient

    else:
        reply_form = ReplyForm()
    context = {
        'reply_form' : reply_form,
    }

    return render(request, template_name, context)

def application_detail(request, message_id, template_name = 'gigs/applier/application_detail.html'):
    """ returns application details """
    application = get_object_or_404(Application, id = message_id)
    print application.body
    if (application.sender != request.user) and (application.recipient != request.user):
        raise Http404
    if application.read_at is None and application.recipient == request.user:
        application.read_at = now()
        application.save()
        if notification:
            notification.send([application.sender], "applications_read")
    application_followup = application_messages(application, user = request.user, application_followup = [])

    context ={
        'application' : application,
        'application_followup' : application_followup,
    }
    return render(request, template_name, context)
 
def application_follower(request, sign, id, template_name = 'gigs/applier/application_detail.html'):
    """ Browse to the next/previous application"""
    app = get_object_or_404(Application, id = id)
    if sign == 'previous':
        # and app has_next()
        # application.next()
        follower_id = app.id - 1
    if sign == 'next':
        follower_id = app.id + 1
    application = Application.objects.filter(gig = app.gig, id = follower_id)
    context ={
        'application' : application,
        
    }
    return render(request, template_name, context)

def application_accept(request):
    """ Flag the application as favorited or rejected"""
    app = get_object_or_404(Application, id = int(request.GET['id']))
    if request.is_ajax():
        action = request.GET['action']
        if action == 'Favorite' and not app.favorited_at:
            app.favorited_at = now()
            app.save()
            message = 'Added to favorites'
        if action == 'Reject':
            app.rejected_at = now()
            app.save()
            message = 'Added to rejected'
    response = simplejson.dumps({
        'message' :  message,
                })
    return HttpResponse(response, content_type='application/javascript')

#Account
def account(request, template_name = 'gigs/account.html'):
    context = {}
    return render(request, template_name, context)

@login_required
def set_notifications(request, template_name = 'gigs/company/account_notifications.html'):
    """
    Handle settings the notifications per user
    logic followed : We set the new notice_setting based on
    the notice_setting's in the request post,if it is found or not 
    in the default notice_settings of the user
    """
    # returning notice_settings except welcome_user
    notice_settings = request.user.noticesetting_set.all().exclude(notice_type__label__exact = 'welcome_user')

    if request.method == 'POST':
        post_keys = request.POST.keys()

        for notice_setting in notice_settings:
            notice_setting_object = NoticeSetting.objects.filter(user = request.user)\
                .filter(notice_type = notice_setting.notice_type)[0]
            if notice_setting.notice_type.label in post_keys:
                notice_setting_object.send = True
            else:
                notice_setting_object.send = False
            notice_setting_object.save()
        notice_settings = request.user.noticesetting_set.all().exclude(notice_type__label__exact = 'welcome_user')
        message = _('Your changes are saved')
        info(request, message, extra_tags='success')

    context = {
        'notice_settings' : notice_settings,
    }
    return render(request, template_name, context)


# Set DEFAULT USER SETTINGS

def set_user_settings(notification_settings, user):
    for notice_type in notification_settings:
        print notice_type
        notice_type_obj = notification.NoticeType.objects.get(label = notice_type)
        print notice_type_obj
        try:
            notification.NoticeSetting(user = user, 
                notice_type = notice_type_obj, medium = '0', send = True).save()
        except:
            pass

@receiver(user_added_to_group, sender = 'apply')
@receiver(user_added_to_group, sender = 'post_job')
def set_user_default_settings(sender, **kwargs):
    user = kwargs['user']
    group = kwargs['group']
    print kwargs
    # set General USER_NOTIFICATION_SETTINGS
    set_user_settings(settings.USER_NOTIFICATION_SETTINGS, user)
    print user
    print user.groups.all()

    # set specific USER_NOTIFICATION_SETTINGS
    if group == 'JobSeeker':
    #if not user.company:
        set_user_settings(settings.JOB_SEEKER_NOTIFICATION_SETTINGS, user)
    if group == 'Company':
    #else:
        set_user_settings(settings.COMPANY_NOTIFICATION_SETTINGS, user)


@receiver(user_added_to_group, sender = 'apply')
@receiver(user_added_to_group, sender = 'post_job')
def welcome_user(sender, **kwargs):
    user = kwargs['user']
    if notification:
        notification.send([user], "welcome_user")
    # Send a welcome Message to Inbox 
    # refer to Company Post a Job -2 
    subject = 'hello there'
    body = loader.get_template('django_messages/welcome_to_inbox.html')
    context = Context({
        'message' : 'something',
        })
    sender = User.objects.filter(username = 'admin')[0]
    message = Message(subject = subject, body = body.render(context),
        sender = sender, recipient = user)
    message.save()









