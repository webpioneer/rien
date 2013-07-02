from django.db import models


class ActiveManager(models.Manager):
	def get_queryset(self):
		return super(ActiveManager, self).get_queryset().filter()

