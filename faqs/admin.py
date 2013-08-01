from django.contrib import admin

from faqs.models import Faq

#class FaqCategoryAdmin(admin.ModelAdmin):
#    list_display = ('title',)

class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'content',)

#admin.site.register(FaqCategory, FaqCategoryAdmin)
admin.site.register(Faq, FaqAdmin)

