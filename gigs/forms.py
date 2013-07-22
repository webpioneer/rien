import logging


from django import forms
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.forms import TinyMceWidget

from gigs.models import Category, Company, Gig, GigType
from mezzanine.accounts.forms import ProfileForm

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
            'area_level3', 'area_level4', 'is_remote', 'content', 'perks',
            'how_to_apply', 'via_email', 'via_url', 'apply_instructions', 'job_type', 
            #'gig_categories',
        ]
 
    def get_gig_object(self):
        """
        Return a new (unsaved) Gig object based on the info in this form.
        Does not set any of the fields that would come from a Request object
        (i.e. ``user`` or ``ip_address``
        """
        GigModel = self.get_gig_model()
        print self.get_gig_create_data()
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
            area_level3 = self.cleaned_data['area_level3'],
            area_level4 = self.cleaned_data['area_level4'],
            is_relocation = self.cleaned_data['is_relocation'],
            is_remote = self.cleaned_data.get('is_remote', True),
            content = self.cleaned_data['content'],
            perks = self.cleaned_data.get('perks',''),
            how_to_apply = self.cleaned_data['how_to_apply'],
            via_email = self.cleaned_data.get('via_email', ''),
            via_url = self.cleaned_data.get('via_url', ''),
            apply_instructions = self.cleaned_data.get('apply_instructions', ''),
            #gig_categories = self.cleaned_data['gig_categories'],
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
            'twitter_username',
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
            twitter_username = self.cleaned_data['twitter_username'],
        )

    def get_company_object(self):
        """
        """
        CompanyModel = self.get_company_model()
        new = CompanyModel(**self.get_company_create_data())

        return new

class ApplyForm(forms.Form):
    motivation = forms.CharField(widget= forms.Textarea)
    resume = forms.FileField()

    def clean_resume(self):
        file = self.cleaned_data['resume']
        if file:
            file_type = file.content_type.split('/')[1]
            print file_type

            if len(file.name.split('.')) == 1:
                raise forms.ValidationError(_('File type is not supported'))

            if file_type in settings.TASK_UPLOAD_FILE_TYPES:
                if file._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
                    raise forms.ValidationError(_('Please keep file size under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
            else:
               raise forms.ValidationError(_('File type is not supported'))
            
        return file

class ProfileForm2(forms.ModelForm):

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'email',)
        #exclude = ('username', 'password2', )

    def __init__(self, *args, **kwargs):
        super(ProfileForm2, self).__init__(*args, **kwargs)
        user_fields = User._meta.get_all_field_names()
        #self.fields['username'] = self.fields['email']
        for field in self.fields:
            # Make user fields required.
            if field in user_fields:
                self.fields[field].required = True

    # Add user to the JobSeeker group
    def _add_to_job_seeker_group(self, user):
        job_seeker_group = Group.objects.get(name = 'JobSeeker')
        user.groups.add(job_seeker_group)

    def clean_email(self):
        """
        Ensure the email address is not already registered.
        """
        email = self.cleaned_data.get("email")
        try:
            User.objects.exclude(id=self.instance.id).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(_("This email is already registered"))

    def save(self, *args, **kwargs):
        """
        Create the new user using their email address as their username.
        """

        password = User.objects.make_random_password()
        print password
        user = User(username = self.cleaned_data['email'], 
            email = self.cleaned_data['email'],
            last_name = self.cleaned_data['last_name'], first_name = self.cleaned_data['first_name'])
        user.set_password(password)
        user.save()
        self._add_to_job_seeker_group(user)

        return user, password

class ReplyForm(forms.Form):
    reply = forms.CharField()
