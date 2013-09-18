from django import template

register = template.Library()

@register.inclusion_tag('feedb/feedbacks_list.html')
def feedbacks_for(obj):
	feedbacks = obj.feedbacks.all().order_by('-submit_date')
	return {
	'feedbacks' : feedbacks,
	'obj' : obj,
	}

