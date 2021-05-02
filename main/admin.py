from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .models import Course
# Register your models here.
admin.site.register(Course)
admin.site.register(Review)

 
# @admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    pass