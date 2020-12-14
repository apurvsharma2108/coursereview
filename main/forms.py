from django import forms
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=('name','site','type','price','AverageRating','description','realse_Date','image')

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=("comment","rating")
