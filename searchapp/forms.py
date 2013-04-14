from django import forms

from searchapp.models import GigSearch

class GigSearchForm(forms.ModelForm):
    class Meta:
        model = GigSearch
        fields = ('what', 'location', )

    def __init__(self, *args, **kwargs):
    	super(GigSearchForm,self).__init__(*args, **kwargs)
    	what_default = 'Job title, Keywords, Company name, ...'
    	self.fields['what'].widget.attrs['placeholder'] = what_default
    	self.fields['what'].widget.attrs['class'] = 'span5'
    	location_default = 'City, State or Zip code'
    	self.fields['location'].widget.attrs['placeholder'] = location_default
    	self.fields['location'].widget.attrs['class'] = 'span5'



    
