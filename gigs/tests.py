from django.test import TestCase
from django.utils import timezone

from gigs.models import Category
from gigs.models import Company
from gigs.models import Gig

class CategoryModelTest(TestCase):
    """
    Test for Category model (Slugged)
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

class CompanyModelTest(TestCase):
    """
    Test for Company model (Displayable, Ownable)
    """
    def _create_user(self):
        pass

    def test_can_create_company_and_save_it(self):
        #create user
        self._create_user()
        #create company
        company = Company()
        company.type = 'Startup'
        company.title = 'Alpha'
        #title is confidential is not required  
        company.title_is_confidential = False
        company.url = 'http://www.google.com'
        company.elevator_pitch = 'elevator pitch'
        company.profile_picture = 'company_logos/logo.png'
        # TO DO : enable for ip_v6 
        company.ip_address = '127.0.0.1'
        # create user
        #self._create_user()
        #company.user = user
        #check save
        company.save()

        #check it's in db and has the right attributes
        companies = Company.objects.all()
        company_in_db = companies[0]
        self.assertEquals(len(companies), 1)
        self.assertEquals(company_in_db.type, 'Startup')
        self.assertEquals(company_in_db.title, 'Alpha')
        self.assertEquals(company_in_db.title_is_confidential, False)
        self.assertEquals(company_in_db.url, 'http://www.google.com')
        self.assertEquals(company_in_db.elevator_pitch, 'elevator pitch')
        self.assertEquals(company_in_db.profile_picture.path, 'company_logos/logo.png')
        self.assertEquals(company_in_db.ip_address, '127.0.0.1')


class GigModelTest(TestCase):
    """
    Test for Gig model
    """
    def _create_category(self):
        category = Category()
        category.title = 'UI Design (Visual Design, user experience, ...'
        category.pub_date = timezone.now()
        category.custom = True
        category.save()

    def test_can_create_a_gig_and_save_it(self):
        #create a category
        self._create_category()
        #create a gig
        gig = Gig()
        gig.title = ' Python / Django developer'
        gig.content = ' This is the content'
        gig.location = ' Chicago, California, usa'
        gig.latitude = 41.87811360
        gig.longitude = -87.62979820
        gig.relocation = True
        gig.is_onsite = True
        gig.perks = 'We provide these perks'
        gig.category = category
        gig.company = company
        # check you can save it
        gig.save()

        # check it saved with its attributes
