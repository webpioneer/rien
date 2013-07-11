from django.contrib import admin

from searchapp.models import GigSearch

class GigSearchAdmin(admin.ModelAdmin):
    list_display = ('what', 'location')

admin.site.register(GigSearch, GigSearchAdmin)

