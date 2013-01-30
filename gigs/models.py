from django.db import models

class Category(models.Model):
    """
    Job Category
    """
    name = models.CharField(max_length = 200)
    pub_date = models.DateTimeField(auto_now_add = True)
    is_custom = models.BooleanField(default = False)

    def __unicode__(self):
        return self.name, self.pub_date
