from django import forms
from .models import *

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields=('name','site','type','price','AverageRating','description','realse_Date','image','Rating','financial_aid','Language','students_enrolled')

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=("comment","rating")

class CourseData(forms.Form):
	class meta:
		model = Course
		fields = '__all__'