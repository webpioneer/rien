"""
Signals relating to adding a user to a group.
The purpose is to assign Notice settings to the user once 
the user is added to a group (categorized)
"""
from django.dispatch import Signal

# Sent just after a user is added to a group
user_added_to_group = Signal(providing_args=["user", "group"])

# Sent after a gig is validated
gig_is_validated = Signal(providing_args=['gig',])

