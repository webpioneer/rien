from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.views import render

from contact.forms import ContactForm

def contact(request, template_name = 'contact/contact.html'):
	if request.method == 'POST':
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			if request.user.is_authenticated():
				contact_form.save(request.user)
			else:
				contact_form.save()
			messages.info(request, _("<strong>Message Sent Successfully</strong>. We will be in touch shortly."),
			 extra_tags='success')
	else:
		contact_form = ContactForm()
	context = {
		'contact_form' : contact_form,
	}
	return render(request, template_name, context)
