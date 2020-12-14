
from django.urls import path
from . import views

app_name="main"

urlpatterns = [
    path('',views.home,name="home"),
    path('details/<int:id>/',views.detail,name="detail"),
    path('addcourses/',views.add_courses,name="add_courses"),
    path('editcourses/<int:id>/',views.edit_courses,name="edit_courses"),
    path('deletecourses/<int:id>/',views.delete_courses,name="delete_courses"),
    path('addreview/<int:id>/',views.add_review,name="add_review"),
    path('editreview/<int:course_id>/<int:review_id>/',views.edit_review,name="edit_review"),
    path('comparecourses/',views.compare_courses,name="compare_courses"),
    path('deletereview/<int:course_id>/<int:review_id>/',views.delete_review,name="delete_review")

]
