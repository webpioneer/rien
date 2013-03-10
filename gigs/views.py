from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from cartridge.shop.views import cart
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
            # save company first
            company = company_form.get_company_object()
            company.ip_address = request.META['REMOTE_ADDR']
            # save gig
            gig = post_job_form.get_gig_object()
            gig.company = company
            # categories
            categories = post_job_form.cleaned_data['categories']
            if 'Preview your listing' == request.POST['submit']:
                print 'preview'
                request.session['company'] = company
                request.session['gig'] = gig
                request.session['categories'] = categories
                template_name = 'gigs/post_job_preview.html'
                context = {
                    'company' : company,
                    'gig' : gig,
                    'categories' : categories,
                }
                print context
                return render(request, template_name, context)
        elif 'Continue to cart' == request.POST['submit']:
            print 'hello'
            company = request.session['company']
            gig = request.session['gig']
            categories = request.session['categories']
            # save company
            company.save()
            # save gig
            gig.company = company
            gig.save()
            for category in categories:
                gig.categories.add(category)
                context = {}
            return redirect("shop_cart")
    else:
        post_job_form = PostJobForm()
        company_form = CompanyForm()
    context = {
        'categories' : Category.objects.all(),
        'post_job_form': post_job_form, 'company_form': company_form,
        'gig_types': gig_types,
        'title': _('Create Your Job Listing'),
        'company_information': _('Company Information'),
        }
    return render(request, template_name, context)
