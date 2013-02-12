from django.test import TestCase
from django.utils import timezone

from mezzanine.core.fields import FileField

from gigs.models import Category
from gigs.models import Company
from gigs.models import Gig
from gigs.models import GigStat

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
    def setUp(self):
        self._category1 = self._create_category()
        self._category2 = self._create_category()
        self._company = self._create_company()

    def _create_category(self):
        category = Category()
        category.title = 'UI Design (Visual Design, user experience, ...'
        category.pub_date = timezone.now()
        category.custom = True
        category.save()
        return category

    def _create_company(self):
        company = Company()
        company.type = 'Startup'
        company.url = 'http://www.alpha.com'
        company.elevator_pitch = 'Elevator pitch content'
        company_profile_picture_field = FileField()
        company_profile_picture = company_profile_picture_field.path = 'company_logo.png'
        company.profile_picture = company_profile_picture
        company.ip_address = '127.0.0.1'
        company.save()
        return company

    def test_can_create_a_gig_and_save_it(self):
        #create a gig
        gig = Gig()
        gig.type = 'Full-time $249'
        gig.title = ' Python / Django developer'
        gig.content = ' This is the content'
        gig.location = ' Chicago, California, usa'
        gig.latitude = '41.87811360'
        gig.longitude = '-87.62979820'
        gig.is_relocation = True
        gig.is_onsite = True
        gig.perks = 'We provide these perks'
        gig.is_filled = False
        #gig.category = self.category
        gig.company = self._company
        # check you can save it
        gig.save()
        # Associate the gig with the Categories
        gig.categories.add(self._category1)
        gig.categories.add(self._category2)

        #check that gig is saved with the right attributes
        gigs_in_db = Gig.objects.all()
        gig_in_db = gigs_in_db[0]
        self.assertEquals(len(gigs_in_db), 1)
        self.assertEquals(gig_in_db.type, 'Full-time $249')
        self.assertEquals(gig_in_db.title, ' Python / Django developer')
        self.assertEqual(gig_in_db.content, ' This is the content')
        self.assertEqual(gig_in_db.location, ' Chicago, California, usa')
        self.assertEqual(gig_in_db.latitude, '41.87811360')
        self.assertEqual(gig_in_db.longitude, '-87.62979820')
        self.assertEqual(gig_in_db.is_relocation, True)
        self.assertEqual(gig_in_db.is_onsite, True)
        self.assertEqual(gig_in_db.perks, 'We provide these perks')
        self.assertEqual(len(gig_in_db.categories.all()), 2)
        self.assertEqual(gig_in_db.company, self._company)


class GigStatTest(TestCase):
    """
    GigStat TestCase
    """
    def test_can_create_gig_stat_and_save_it(self):
        gig_stat = GigStat()
        gig_stat.views = 100
        gig_stat.clicked_apply = 80
        gig_stat.notified_users = 300
        gig_stat.save()

        # check it's saved with its attributes
        gig_stats = GigStat.objects.all()
        gig_stat_in_db = gig_stats[0]
        self.assertEqual(len(gig_stats), 1)
        self.assertEqual(gig_stat_in_db.views, 100)
        self.assertEqual(gig_stat_in_db.clicked_apply, 80)
        self.assertEqual(gig_stat_in_db.notified_users, 300)
