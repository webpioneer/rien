from django.http import Http404

from mezzanine.utils.views import render

from faqs.models import Faq

def faqs_list(request, template_name = 'faqs/faqs_list.html'):
	"""
	returns a list of published FAQs
	"""
	try:
		faqs = Faq.objects.published()
	except:
		raise Http404
	context = {
		'faqs' : faqs,
	}
	return render(request, template_name, context)