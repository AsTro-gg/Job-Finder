from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(JobSeekerModel)
admin.site.register(EmployerModel)
admin.site.register(AppliedTo)