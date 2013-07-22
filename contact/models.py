from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	name = models.CharField(max_length = 255)
	email = models.EmailField()
	subject = models.CharField(max_length = 255)
	message = models.TextField()
	user = models.ForeignKey(User, blank = True, null = True)

	def __unicode__(self):
		return '{0} : {1}'.format(self.email, self.subject)
