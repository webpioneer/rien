from django.contrib import admin

from gigs.models import Category, GigType

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')

class GigTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'price',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(GigType, GigTypeAdmin)
