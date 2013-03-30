from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cartridge.shop.forms import AddProductForm
from cartridge.shop.models import (Cart, CartItem, Product,
 ProductImage, ProductVariation)
from cartridge.shop.views import cart, product as product_view

from mezzanine.utils.views import render

from gigs.forms import CompanyForm, PostJobForm
from gigs.models import Category, GigType

def post_job(request, template_name = 'gigs/post_job.html'):
    """ 
    Post Job Form 
    """
    gig_types = GigType.objects.all()
    if request.method == 'POST':
        post_job_form = PostJobForm(request.POST)
        company_form = CompanyForm(request.POST)
        #post_job_form_data = post_job_form.get_gig_create_data()

        if  post_job_form.is_valid() and company_form.is_valid():
            print 'forms are valid'
            # save company first
            company = company_form.get_company_object()
            company.ip_address = request.META['REMOTE_ADDR']
            #company.profile_picture = company_form.cleaned_data['profile_picture']
            company.profile_picture = request.FILES.get('profile_picture', '')
            company.save()
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
                gig.unit_price = 100.0
                gig.sku = gig.id
                gig.image = company.profile_picture
                gig.save()
                gig_variation = ProductVariation(product = gig, default = True,
                 unit_price = gig.job_type.price.amount, sale_price = gig.job_type.price.amount)
                gig_variation.save()
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
