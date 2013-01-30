from django.test import TestCase
from django.utils import timezone

from gigs.models import Category
#from gigs.models import Gig

class CategoryModelTest(TestCase):
    """
    Test for Category model
    """
    def test_can_create_a_category_and_save_it(self):
        #check we can create a category
        category = Category()
        category.title = 'UI Design (Visual Design, user experience, ...'
        category.pub_date = timezone.now()
        category.custom = True
        #check that it can be saved
        category.save()

        #check it exists in db
        categories = Category.objects.all()
        category_in_db = categories[0]
        self.assertEquals(len(categories), 1)
        self.assertEquals(category_in_db, category)

        #check it saved with attributes
        self.assertEquals(category_in_db.title, category.title)
        self.assertEquals(category_in_db.pub_date, category.pub_date)
    
