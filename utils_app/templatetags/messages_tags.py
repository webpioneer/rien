from django import template
from django_messages.models import Message
from collections import deque

register = template.Library()

def get_parents(message, messages_list):
	parent_message = getattr(message, 'parent_msg', False)
	if isinstance(parent_message, Message):
		messages_list.append(parent_message)
		get_parents(parent_message, messages_list)

@register.inclusion_tag('utils_app/message_family.html')
def message_family(message):
	messages_list = []
	get_parents(message, messages_list)
	return {'messages' : messages_list}
