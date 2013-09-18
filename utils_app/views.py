from django.contrib.auth.models import User
from django.contrib.messages import info
from django.core import mail
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _

from mezzanine.utils.views import render

from gigs.models import Application
from utils_app.forms import ResumeForm, PeopleForm, TeamForm
from utils_app.models import EmailedResume, GroupWithType, Team

def email_resume(request, attach, template_name = 'utils_app/email_resume.html'):
	app = Application.objects.get(id = request.POST.get('application_id'))
	if request.method == 'POST':
		resume_form = ResumeForm(request.POST)
		
		if resume_form.is_valid():
			post_data = resume_form.cleaned_data
			emailed_resume = EmailedResume()
			emailed_resume.recipients = post_data.get('recipients')
			emailed_resume.subject = post_data.get('subject')
			emailed_resume.body = post_data.get('body')
			emailed_resume.sender = request.user
			
			emailed_resume.application = app
			emailed_resume.save()
			# send the email(s)
			connection = mail.get_connection()
			connection.open()
			print emailed_resume.recipients.split(',')
			if ',' in emailed_resume.recipients:
				print 'in'
				emails = [ mail.EmailMessage(emailed_resume.subject,
					 emailed_resume.body, emailed_resume.sender.email,
		                          [recipient])
					for recipient in emailed_resume.recipients.split(',') ]

				for email in emails:
					email.attach_file(app.resume.file.path)
				#print emails[0].attach_file(app.resume.file.path)
				#emails_attached = [	email.attach_file(app.resume.file.path) for email in emails ]
				#print emails_attached
				connection.send_messages(emails)
				connection.close()
			else:
				print 'not in '
				message = EmailMessage(emailed_resume.subject, emailed_resume.body, emailed_resume.sender.email, [emailed_resume.recipients])
				if attach == 'True':
					message.attach_file(app.resume.file.path)
				message.send()
			if attach == 'True':
				message = _("The applicant's resume was emailed to the <strong>%s</strong>." %
					emailed_resume.recipients)
			else:
				message = _('Feedback on <strong>%s</strong> requested from <strong>%s</strong>'
					 % (app.sender.last_name.capitalize(), emailed_resume.recipients))
			info(request, message, extra_tags='success')
			return redirect(app.get_absolute_url())
			
	else:
		resume_form = ResumeForm()
	context = {
		'resume_form' : resume_form,
		'application' : app,
	}
	if attach == 'True':
		context['attach'] = True
	return render(request, template_name, context)


def people(request, template_name = 'utils_app/people.html'):
	# retrieve user (owner) as it is need in POST and GET 
	owner = request.user
	#people_groups = [ (user, user.groups.all()[0].groupwithtype.group_type) for group in owner.groupwithtypes.all()
	#	 for user in group.user_set.all().order_by('-date_joined') ]
	if request.method == 'POST':
		people_form = PeopleForm(request.POST)
		team_form = TeamForm(request.POST)
		if people_form.is_valid():
			#retrieve post data
			post_data = request.POST.copy()
			print post_data
			account_type = post_data['account_type']
			email = post_data['email']
			last_name = post_data['last_name']
			first_name = post_data['first_name']
			# check if group type already exists, otherwise create a new group type
			group_type, group_type_created = GroupWithType.objects.get_or_create(
			 name = '%s_%s' % (account_type, owner.id), group_type = account_type, user = owner)
			print group_type, group_type_created
			# create a new user
			new_user_password = User.objects.make_random_password()
			new_user = User.objects.create_user(username = email, email = email,
                        password = new_user_password)
			new_user.last_name = last_name
			new_user.first_name = first_name
			new_user.save()
			# add the new user to the group type
			new_user.groups.add(group_type)
			# send email to the new user with a randomly generated password and link

			# send message
			message = _('User <strong>%s</strong> (%s) account was created. An email is sent to <strong>%s</strong> to notify him'
					 % (new_user, group_type.group_type, email))
			info(request, message, extra_tags='success')
			return redirect(request.META['HTTP_REFERER'])
		else:
			context ={
				'people_form' : people_form,
				'people_form' : people_form,
			}
		
		if team_form.is_valid():
			#create a group if it does not exist
			post_data = request.POST.copy()
			team_name = post_data['team_name']
			#team, team_created = Team.objects.get_or_create(
			# name = team_name, user = owner)
			# send message
			message = _('Team <strong>%s</strong> was created' % team_name)
			info(request, message, extra_tags='success')
			return redirect(request.META['HTTP_REFERER'])
		else:
			context = {
				'team_form' : team_form,
				'people_form' : people_form,
			}

	else:
		people_form = PeopleForm()
		team_form = TeamForm()
		context = {
			'people_form' : people_form,
			'team_form' : team_form,
		}
	#context['people_groups'] = people_groups
		
	return render(request, template_name, context)
	
