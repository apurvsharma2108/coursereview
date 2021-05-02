from import_export import resources
from .models import Course

class CourseResource(resources.ModelResource):
    class meta:
        model=Course