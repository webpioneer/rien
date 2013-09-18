#from django.contrib.contenttypes.models 
from django.contrib.messages import info
from django.contrib.sites.models import Site
from django.db.models import get_model
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.sites import current_site_id
from mezzanine.utils.views import render

from feedb.models import Feedback
from feedb.forms import FeedbackForm

def submit_feedback(request, app_name = None, model_name = None, id = None, template_name = 'feedb/submit_feedback.html'):
	"""
	handles submitting feedback regardless of the object type
	"""
	if request.method == 'POST':
		feedback_form = FeedbackForm(request.POST)
		obj_id = request.POST['obj']
		model_name = request.POST['model_name']
		app_name = request.POST['app_name']
		model = get_model(app_name, model_name)
		obj = model.objects.get( id = obj_id )
		if feedback_form.is_valid():
			print 'form is valid'
			post_data = feedback_form.cleaned_data
			

			feedback = Feedback(content_object = obj, user = request.user)
			feedback.feedback = post_data['feedback']
			feedback.rating = post_data['rating']
			feedback.site = Site.objects.get(id = current_site_id())
			feedback.save()
			message = _('Feedback on <strong>%s</strong> application is saved.' % obj.sender.get_full_name().capitalize())
			info(request, message, extra_tags='success')
			return redirect(obj.get_absolute_url())
		else:
			context = {
			'feedback_form' : feedback_form,
			'obj' : obj,
			'model_name' : model_name,
			'app_name' : app_name,
			}
			template_name = request.META['HTTP_REFERER']
			#return render(request, template_name, context)
			return redirect(obj.get_absolute_url(), context)

	else:
		model = get_model(app_name, model_name)
		obj = model.objects.get( id = id )
		feedback_form = FeedbackForm()
	context = {
		'feedback_form' : feedback_form,
		'obj' : obj,
		'model_name' : model_name,
		'app_name' : app_name,
	}

	return render(request, template_name, context)

