from django import forms
from contact.models import Contact

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['user',]

    def save(self, user = None, commit = True):
    	instance = super(ContactForm, self).save(commit=False)
    	if user:
    		instance.user = user
    	if commit:
        	instance.save()
    	return instance