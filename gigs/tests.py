from moneyed import Money, USD

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from mezzanine.core.fields import FileField

from gigs.models import Category
from gigs.models import Company
from gigs.models import Gig
from gigs.models import GigType
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
    
    def test_can_create_company_and_save_it(self):
        #create user
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
        # a user is created along through the Company.save()
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
        self.assertEqual(company_in_db.user, company.user)
        self.assertEqual(company_in_db.user.email, company.email)


class GigTypeTest(TestCase):
    """
    Test for the Type of Gig
    """
    def test_create_gigtype_and_save_it(self):
        # check you can create a type and save it
        gig_type = GigType()
        gig_type.type = 'Full-time'
        gig_type.description = 'Salaried position, ...'
        gig_type.price = Money(249, USD)
    
        # check it can be saved
        gig_type.save()

        # check it's saved with attributes
        gig_types = GigType.objects.all()
        gig_type_in_db = gig_types[0]
        self.assertEquals(len(gig_types), 1)
        self.assertEquals(gig_type_in_db.type, 'Full-time')
        self.assertEquals(gig_type_in_db.description, 'Salaried position, ...')
        self.assertEquals(gig_type_in_db.price, Money(249, USD))

class GigModelTest(TestCase):
    """
    Test for Gig model
    """
    def setUp(self):
        self._category1 = self._create_category()
        self._category2 = self._create_category()
        self._company = self._create_company()
        self._gig_type = self._create_gig_type()

    def _create_category(self):
        category = Category()
        category.title = 'UI Design (Visual Design, user experience, ...'
        category.pub_date = timezone.now()
        category.custom = True
        category.save()
        return category

    def _create_company(self):
        company = Company()
        company.title = 'Alpha'
        company.type = 'Startup'
        company.url = 'http://www.alpha.com'
        company.elevator_pitch = 'Elevator pitch content'
        company_profile_picture_field = FileField()
        company_profile_picture = company_profile_picture_field.path = 'company_logo.png'
        company.profile_picture = company_profile_picture
        company.ip_address = '127.0.0.1'
        company.save()
        return company
    
    def _create_gig_type(self):
        gig_type = GigType()
        gig_type.type = 'Full-time'
        gig_type.description = 'Salaried position, ...'
        gig_type.price = Money(249, USD)
        gig_type.save()
        return gig_type

    def test_can_create_a_gig_and_save_it(self):
        #create a gig
        gig = Gig()
        gig.type = self._gig_type
        gig.title = ' Python / Django developer'
        gig.content = ' This is the content'
        gig.location = ' Chicago, California, usa'
        gig.latitude = '41.87811360'
        gig.longitude = '-87.62979820'
        gig.is_relocation = True
        gig.perks = 'Free food'
        gig.how_to_apply = Gig.HOW_TO_APPLY_CHOICES[0][0]
        if gig.how_to_apply == Gig.HOW_TO_APPLY_CHOICES[0][0]:
            gig.via_email = 'contact@myemail.com'
        elif gig.how_to_apply == Gig.HOW_TO_APPLY_CHOICES[0][1]:
            gig.via_url = 'http://www.google.com'
        gig.apply_instructions = 'Apply by email'
        gig.is_onsite = True
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
        self.assertEquals(gig_in_db.type, self._gig_type)
        self.assertEquals(gig_in_db.title, ' Python / Django developer')
        self.assertEqual(gig_in_db.content, ' This is the content')
        self.assertEqual(gig_in_db.location, ' Chicago, California, usa')
        self.assertEqual(gig_in_db.latitude, '41.87811360')
        self.assertEqual(gig_in_db.longitude, '-87.62979820')
        self.assertEqual(gig_in_db.is_relocation, True)
        self.assertEqual(gig_in_db.perks, 'Free food')
        self.assertEqual(gig_in_db.how_to_apply, Gig.HOW_TO_APPLY_CHOICES[0][0])
        self.assertEqual(gig_in_db.via_email, 'contact@myemail.com')
        self.assertEqual(gig_in_db.apply_instructions, 'Apply by email')
        self.assertEqual(gig_in_db.is_onsite, True)
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
