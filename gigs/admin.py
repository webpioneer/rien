from django.contrib import admin

from gigs.models import Category, ChildStatus, Company, Gig, GigType

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')

class GigTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'price',)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'email',)

class GigAdmin(admin.ModelAdmin):
    list_display = ('job_type', 'title',)

class ChildStatusAdmin(admin.ModelAdmin):
	list_display = ('name', 'date', 'user')

admin.site.register(Category, CategoryAdmin)
admin.site.register(GigType, GigTypeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Gig, GigAdmin)
admin.site.register(ChildStatus, ChildStatusAdmin)
