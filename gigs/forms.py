import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.forms import TinyMceWidget

from gigs.models import Category, Company, Gig, GigType

class PostJobForm(forms.ModelForm):
    """ 
    Model form for Gig model 
    """
    title = forms.CharField(label = _('Job Title'), max_length = 255)
    
    class Meta:
        model = Gig
        
        fields = [
            'job_type', 'gig_categories', 'title', 'location', 'latitude', 
            'longitude', 'is_relocation', 'area_level1', 'area_level2',
            'is_onsite', 'content', 'perks', 'how_to_apply', 'via_email',
            'via_url', 'apply_instructions',
        ]
 
    def get_gig_object(self):
        """
        Return a new (unsaved) Gig object based on the info in this form.
        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``
        """
        GigModel = self.get_gig_model()
        gig = GigModel(**self.get_gig_create_data())
        
        return gig

    def get_gig_model(self):
        """
        Get the Gig model to create with this form.
        """
        return Gig
    
    def get_gig_create_data(self):
        """
        Returns the dict of data to be used to create a Gig
        """
         
        return dict(
            job_type = self.cleaned_data['job_type'],
            title = self.cleaned_data['title'],
            location = self.cleaned_data['location'],
            latitude = self.cleaned_data['latitude'],
            longitude = self.cleaned_data['longitude'],
            area_level1 = self.cleaned_data['area_level1'],
            area_level2 = self.cleaned_data['area_level2'],
            is_relocation = self.cleaned_data['is_relocation'],
            is_onsite = self.cleaned_data.get('is_onsite', True),
            content = self.cleaned_data['content'],
            perks = self.cleaned_data.get('perks',''),
            how_to_apply = self.cleaned_data['how_to_apply'],
            via_email = self.cleaned_data.get('via_email', ''),
            via_url = self.cleaned_data.get('via_url', ''),
            apply_instructions = self.cleaned_data.get('add-instructions', ''),
        )

    def _add_categories_to_gig(self, gig):
        for posted_category in self.cleaned_data['categories']:
            gig.categories.add(category)


class CompanyForm(forms.ModelForm):
    """
    Model form for Company model
    """
    profile_picture = forms.ImageField(required = False, label = _('Profile Picture'))
    
    class Meta:
        model = Company
        fields = (
            'type', 'company_name', 'title_is_confidential', 'url', 'email',
            'elevator_pitch', 'profile_picture_choice', 'profile_picture',
            )
    
    def get_company_model(self):
        """
        Get the Company model to create with this form
        """
        return Company

    def get_company_create_data(self):

        return dict(
            type = self.cleaned_data['type'],
            company_name = self.cleaned_data['company_name'],
            url = self.cleaned_data['url'],
            email = self.cleaned_data['email'],
            elevator_pitch = self.cleaned_data['elevator_pitch'],
            profile_picture_choice = self.cleaned_data['profile_picture_choice'],
            profile_picture = self.cleaned_data['profile_picture'],
        )

    def get_company_object(self):
        """
        """
        CompanyModel = self.get_company_model()
        new = CompanyModel(**self.get_company_create_data())

        return new
