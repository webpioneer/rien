from django import forms

class FeedbackForm(forms.Form):
	feedback = forms.CharField(max_length=1000, widget = forms.Textarea)
	rating = forms.FloatField(required = False, widget = forms.HiddenInput)
	app_name = forms.CharField(max_length = 100, widget = forms.HiddenInput)
	model_name = forms.CharField(max_length = 100, widget = forms.HiddenInput)
	obj = forms.IntegerField(widget = forms.HiddenInput)