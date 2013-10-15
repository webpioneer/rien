from django.contrib import admin

from searchapp.models import GigSearch

class GigSearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'what', 'location', 'is_onsite', 'subscribed_user')

admin.site.register(GigSearch, GigSearchAdmin)

