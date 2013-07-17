from mezzanine.utils.views import render

from contact.forms import ContactForm

def contact(request, template_name = 'contact/contact.html'):
	if request.method == 'POST':
		if contact_form.is_valid():
			contact_form.save()
	else:
		contact_form = ContactForm()
	context = {
		'contact_form' : contact_form,
	}
	return render(request, template_name, context)
