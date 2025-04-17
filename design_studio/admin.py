from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ClientRequest)
admin.site.register(DesignerApplication)
admin.site.register(Review)
admin.site.register(CompanyInfo)
admin.site.register(WorkStage)
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')