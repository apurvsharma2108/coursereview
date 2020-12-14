from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Course(models.Model):
    name=models.CharField(max_length=500)
    site=models.CharField(max_length=500)
    type=models.CharField(max_length=500)#intermediate high or low #1
    price=models.FloatField()#2
    description=models.TextField(max_length=5000)
    realse_Date=models.DateField()#3
    AverageRating=models.FloatField(default=False)
    image=models.URLField(default=None,null=True)
    # year=models.IntegerField(default=0)
    financial_aid=models.BooleanField(default=False)#4
    students_enrolled=models.IntegerField(default=0) #5
    Language=models.CharField(max_length=500)#6
    Rating=models.FloatField(default=0)#7
    def __str__(self):
        return self.name
    def __unicode__(self):
        return self.name

class Review(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField(max_length=1000)
    rating=models.FloatField(default=0)

    def __str__(self):
        return self.user.username
