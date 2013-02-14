from django.contrib import admin

from gigs.models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    
admin.site.register(Category, CategoryAdmin)
