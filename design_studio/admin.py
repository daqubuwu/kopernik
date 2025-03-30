from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ClientRequest)
admin.site.register(DesignerApplication)
admin.site.register(Review)
admin.site.register(CompanyInfo)
admin.site.register(WorkStage)

