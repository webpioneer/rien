from django import forms
#from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _



from utils_app.models import EmailContentBase, EmailedResume

class ResumeForm(ModelForm):

	body = forms.CharField(widget=forms.Textarea(attrs = {'rows': '5'}))
	class Meta:
		model = EmailedResume
		fields = ['recipients', 'subject', 'body',]

	def clean_recipients(self):
		recipients = self.cleaned_data['recipients']
		print type(recipients)
		if ',' not in recipients:
			validate_email(recipients)
		else:
			recipients_list = recipients.split(',')
			for recipient in recipients_list:
				validate_email(recipient)
		return recipients

TYPE_CHOICES = (
		('INTERVIEWER', _('Interviewer')),
		('RECRUITER', _('Recruiter')),
		#('ADMIN', _('Administrator')),
		)

class PeopleForm(forms.Form):
	
	account_type = forms.ChoiceField(widget = forms.Select(), choices = TYPE_CHOICES,
		initial = TYPE_CHOICES[0][0])
	first_name = forms.CharField(_('First Name'))
	last_name = forms.CharField(_('Last Name'))
	email = forms.EmailField(_('Email'))

class TeamForm(forms.Form):
	team_name = forms.CharField(_('Team'))

