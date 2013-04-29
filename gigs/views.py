from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.messages import info
from django.db.models import Min
from django.shortcuts import HttpResponse, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required



from cartridge.shop.forms import AddProductForm
from cartridge.shop.models import (Cart, CartItem, Product,
 ProductImage, ProductVariation)
from cartridge.shop.views import cart, product as product_view

from mezzanine.conf import settings
from mezzanine.utils.views import paginate, render
from mezzanine.utils.sites import current_site_id
from mezzanine.utils.urls import slugify

from gigs.forms import CompanyForm, PostJobForm
from gigs.models import Category, Gig, GigType
from searchapp.forms import GigSearchForm

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
        if 'shop/product' in request.META['HTTP_REFERER']:
            message = _('Your listing is published successfully. \
            Please visit "%s" to track listing statistics, make edits, and more.') % gig.company.email
            info(request, message)
    except:
        pass
        
    context = {
        'gig' : gig,
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
                #gig.status = 1
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
    print 'company_listings called'
    context = {}
    return render(request, template_name, context)

@login_required
def company_infos(request, template_name ='gigs/company/company_infos.html'):
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
    company = get_object_or_404(Company, slug = slug)
    print company
    context = {'company' : company, }
    return render(request, template_name, context)



