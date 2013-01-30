from django.contrib import admin

from mezzanine.core.admin import DisplayableAdmin, OwnableAdmin

from gigs.models import Category

class CategoryAdmin(DisplayableAdmin, OwnableAdmin):
    list_display = ('name', 'pub_date')
    
admin.site.register(Category, CategoryAdmin)
