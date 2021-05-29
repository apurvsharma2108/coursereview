from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg
from .models import Course
from django.contrib import messages
from .resources import CourseResource
from tablib import Dataset
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render 
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
def home(request):
    query=request.GET.get("title")
    allCourses=None
    if query:
        allCourses=Course.objects.filter(name__icontains=query)
    else:
        allCourses=Course.objects.all()
    
    p=Paginator(allCourses,8)
    page_num=request.GET.get('page',1)



    try:
        page=p.page(page_num)
    except (EmptyPage , PageNotAnInteger,TypeError):                           #if you access a invalid page
        page=p.page(1)


    context={
        'courses':page,
    }
    

    return render(request,'main/index.html',context)
def compare_courses(request):
    query=request.GET.get("title")
    allCourses=None
    if query:
        allCourses=Course.objects.filter(name__icontains=query)
    else:
        allCourses=Course.objects.all()
    context={
        'courses':allCourses,
    }
    return render(request,'main/newindex.html',context)
# details page
def detail(request,id):
    reviews=Review.objects.filter(course=id).order_by("-comment")
    course=Course.objects.get(id=id)
    average=reviews.aggregate(Avg("rating"))["rating__avg"]
    if average==None:
        average=0
    average=round(average,2)
    context={
        "course":course,
        "reviews":reviews,
        "average":average
    }
    return render(request,'main/details.html',context)
def add_courses(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            if request.method == "POST":
                form=CourseForm(request.POST or None)

                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("main:home")
            else:
                form=CourseForm()
            return render(request,'main/addcourses.html',{"form":form,"controller":"Add Courses"})
        else:
            return redirect("main:home")
    return redirect("acounts:login")

def edit_courses(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            course=Course.objects.get(id=id)
            if request.method=="POST":
                form=CourseForm(request.POST or None,instance=course)

                if form.is_valid():
                    data=form.save(commit=False)
                    data.save()
                    return redirect("main:detail",id)
            else:
                form=CourseForm(instance=course)
            return render(request,'main/addcourses.html',{"form":form,"controller":"Edit Courses"})
        else:
            return redirect("main:home")
    return redirect("acounts:login")



def delete_courses(request,id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            course=Course.objects.get(id=id)
            course.delete()
            return redirect("main:home")
        else:
            return redirect("main:home")
    return redirect("acounts:login")





def add_review(request,id):
    if request.user.is_authenticated:
        course=Course.objects.get(id=id)
        if request.method == "POST":
            form=ReviewForm(request.POST or None)
            if form.is_valid():
                data=form.save(commit=False)
                data.comment=request.POST["comment"]
                data.rating=request.POST["rating"]
                data.user=request.user
                data.course=course
                data.save()
                return redirect("main:detail",id)
        else:
            form=ReviewForm()
        return render(request,'main/details.html',{"form":form})
    else:
        return redirect("acounts:login")




def edit_review(request,course_id,review_id):
    if request.user.is_authenticated:
        course=Course.objects.get(id=course_id)

        review=Review.objects.get(course=course,id=review_id)

        if request.user==review.user:
            if request.method=="POST":
                form=ReviewForm(request.POST,instance=review)
                if form.is_valid():
                    data=form.save(commit=False)
                    if (data.rating>10) or (data.rating<0):
                        error="Out of range Please select a valid range between 0 to 10"
                        return render(request,'main/editreview.html',{"error":error,"form":form})
                    else:
                        data.save()
                        return redirect("main:detail",course_id)
            else:
                form=ReviewForm(instance=review)
            return render(request,'main/editreview.html',{"form":form})
        else:
            return redirect("main:detail",course_id)
    else:
        return redirect("acounts:login")

def delete_review(request,course_id,review_id):
    if request.user.is_authenticated:
        course=Course.objects.get(id=course_id)

        review=Review.objects.get(course=course,id=review_id)

        if request.user==review.user:
            review.delete()
                    
           
        return redirect("main:detail",course_id)
    else:
        return redirect("acounts:login")


def export(request):
    course_resource = CourseResource()
    dataset = course_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

def ipt(request):
    return render(request,"main/rinput.html")

def reco(request):
    lis=[]
    lis.append(request.GET['CO'])

    print(lis)

    df = pd.read_csv("complete_course_data.csv")

    features = ["course_title","platform","level"]

    def combine_features(row):
        return row['course_title']+" "+row['platform']+" "+row['level']


    for feature in features:
        df[feature] = df[feature].fillna('') #filling all NaNs with blank string


    df["combined_features"] = df.apply(combine_features,axis=1)
#applying combined_features() method over each rows of dataframe and storing the combined string in "combined_features" column


    cv = CountVectorizer() #creating new CountVectorizer() object
    count_matrix = cv.fit_transform(df["combined_features"]) #feeding combined strings(course contents) to CountVectorizer() object

    cosine_sim = cosine_similarity(count_matrix) #cosine similarity matrix for count matrix

    def get_title_from_index(index):
        return df[df.index == index]["course_title"].values[0]
    def get_index_from_title(title):
        return df[df.course_title == title]["index"].values[0]

    

    course_user_likes =lis[0]  # here take the inputs of user
    course_index = get_index_from_title(course_user_likes)
    similar_courses = list(enumerate(cosine_sim[course_index])) #accessing the row corresponding to given course to find all the similarity scores for that course and then enumerating over it


    sorted_similar_courses = sorted(similar_courses,key=lambda x:x[1],reverse=True)[1:]

    res=[]
    i=0
    print("Top 5 similar courses to "+course_user_likes+" are:\n")
    for element in sorted_similar_courses:
        print(get_title_from_index(element[0]))
        res.append(get_title_from_index(element[0]))
        i=i+1
        if i>5:
            break

    ans=res[1:6]
    return render(request,"main/result.html",{'ans':ans})






























def simple_upload(request):
    if request.method == 'POST':
        course_resource = CourseResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read(),format='xlsx')
        for data in imported_data:
        	value = Course(
        		data[0],
        		data[1],
        		data[2],
        		data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
        		)
        	value.save()     
    return render(request,'upload.html')