from django.shortcuts import render , redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate , login , logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import *
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.urls import reverse


# Create your views here.

def home(request):
    return render(request , 'index.html')

def display_quiz_teacher(request , quiz_id):
    all_ques = quiz_ques.objects.filter(quiz_id = quiz_id)
    context = {'all_ques' : all_ques}
    print(all_ques)
    return render(request , 'display_quiz_teacher.html' , context)

def display_course_teacher(request , course_id):
    course_obj = course.objects.filter(course_id = course_id)
    all_quiz = quiz_desc.objects.filter(course_id = course_id)
    context = {'all_quiz' : all_quiz , 'course_obj' : course_obj}
    return render(request , 'display_course_teacher.html' , context)

def display_created_courses(request):
    all_courses = course.objects.filter(teacher_id = request.user.email)
    # print(all_courses)
    context = {'all_courses' : all_courses}
    return render(request , 'display_created_courses.html' , context)

def teacher_dashboard(request):
    rd = request.session.get('rd')
    if rd==3:
        name = request.user.first_name + " " + request.user.last_name
        messages.info(request, f"You are now logged in as {name}.")
        request.session['rd']=0

    return render(request , 'teacher_dashboard.html')

def set_ques(request  , quiz_id): 
    if request.method == 'POST':
        set_question_form = set_ques_form(request.POST)
        if set_question_form.is_valid():
            ques_text = set_question_form.cleaned_data['ques_text']
            opt1 = set_question_form.cleaned_data['opt1']
            opt2 = set_question_form.cleaned_data['opt2']
            opt3 = set_question_form.cleaned_data['opt3']
            opt4 = set_question_form.cleaned_data['opt4']
            correct_opt = set_question_form.cleaned_data['correct_opt']
            ques_marks = set_question_form.cleaned_data['ques_marks']

            quiz_detail=quiz_desc.objects.get(pk=quiz_id)
            ques_id=str(request.session['cnt'])+"_" +str(quiz_id)

            ques_obj = quiz_ques(ques_text=ques_text , opt1=opt1 , opt2=opt2 , opt3=opt3 , 
                                opt4=opt4 , correct_opt=correct_opt, ques_marks=ques_marks ,
                                quiz_id=quiz_detail , ques_id=ques_id)
            
            ques_obj.save()
            if(request.session['cnt'] == quiz_detail.no_of_ques):
                return redirect('/teacher_dashboard')
            else :
                request.session['cnt']+=1
            
    quiz_detail=quiz_desc.objects.get(pk=quiz_id)
    set_question_form = set_ques_form()
    context = {'form' : set_question_form  , 'ques_no':request.session['cnt'] , 'quiz_detail':quiz_detail}
    return render(request , 'set_ques.html' , context)

def create_quiz(request , course_id):
    if request.method =='POST':
        new_quiz_form = create_quiz_form(request.POST)

        if new_quiz_form.is_valid():
            quiz_title = new_quiz_form.cleaned_data['quiz_title']
            quiz_duration = new_quiz_form.cleaned_data['quiz_duration']
            no_of_ques = new_quiz_form.cleaned_data['no_of_ques']

            quiz_id = course_id+"_" + quiz_title
            # quiz_id = 3
            course_id = course.objects.get(pk = course_id)

            quiz_obj = quiz_desc(quiz_title = quiz_title , quiz_duration = quiz_duration,
                                 no_of_ques = no_of_ques , quiz_id = quiz_id , course_id = course_id)
            
            quiz_obj.save()
            request.session['cnt']=1
            return redirect(reverse('set_ques' ,args=[quiz_id]))
        
    new_quiz_form = create_quiz_form()
    context = {'form' : new_quiz_form , 'course_id' : course_id}
    return render(request , 'create_quiz.html' , context)

def create_new_course(request):
    if request.method == 'POST':
        new_course_form = create_new_course_form(request.POST)
        
        if new_course_form.is_valid():
            course_name = new_course_form.cleaned_data['course_name']
            course_duration = new_course_form.cleaned_data['course_duration']
            category = new_course_form.cleaned_data['category']
            topic = new_course_form.cleaned_data['topic']
            course_material = new_course_form.cleaned_data['course_material']

            publish_date = datetime.now()
            course_id = str(publish_date)+"_" + course_name
            # course_id = "3"
            teacher_id = user_details.objects.get(pk= request.user.email)
            
            course_obj = course(course_name= course_name , course_duration=course_duration , 
                                      category=category , topic=topic , course_material=course_material ,
                                      publish_date=publish_date , course_id=course_id , 
                                      teacher_id=teacher_id)
            
            course_obj.save()
            return redirect(reverse('create_quiz' ,args=[course_id]))

    new_course_form =create_new_course_form()
    # print("new course form")
    # print(new_course_form)
    context = {'form' : new_course_form}
    return render(request , 'create_new_course.html' , context)

@login_required(login_url='/login')
def dashboard(request):
    rd = request.session.get('rd')
    if rd==3:
        name = request.user.first_name + " " + request.user.last_name
        messages.info(request, f"You are now logged in as {name}.")
    return render(request , 'dashboard.html')

def logout_page(request):
    logout(request)
    request.session['rd']=2
    # messages.info(request, "You have successfully logged out.") 
    return redirect('/login/')

def login_page(request):
    rd = request.session.get('rd')
    if rd==1:
        messages.info(request, "Account created successfully")
        request.session['rd']=0
    elif rd==2:
        messages.info(request, "You have successfully logged out.") 
        request.session['rd']=0

    if request.method == "POST":
        login_form = login_user_form(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            print(email)
            print(password)

            user=authenticate(email=email , password=password)

            if user is not None:
                login(request , user)
                request.session['rd']=3
                if request.user.role==1:
                    return redirect('/teacher_dashboard')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")

    login_form = login_user_form()
    # print(login_form)
    context = {'form' : login_form}
        
    return render(request , 'login.html' , context)

def register(request):
    if request.method == 'POST':
        signup_form = user_detail_forms(request.POST)
        if signup_form.is_valid():

            first_name = signup_form.cleaned_data['first_name']
            last_name = signup_form.cleaned_data['last_name']
            email = signup_form.cleaned_data['email']
            password = signup_form.cleaned_data['password']
            dob = signup_form.cleaned_data['dob']
            mobile = signup_form.cleaned_data['mobile']
            address = signup_form.cleaned_data['address']
            role = signup_form.cleaned_data['role']
            institute = signup_form.cleaned_data['institute']
            role_desc = signup_form.cleaned_data['role_desc']

            user_details_obj = user_details(first_name=first_name , last_name=last_name , 
                                            email=email, dob=dob , 
                                            mobile=mobile , address=address , role=role , 
                                            institute=institute , role_desc=role_desc)
            
            user_details_obj.set_password(password)
            user_details_obj.save()
            # signup_form.save()

            request.session['rd']=1
            return redirect('/login/')

    signup_form = user_detail_forms()
    context = {'form' : signup_form}
    return render(request ,  'signup.html' , context)





def signup(request):
    if request.method == "POST":
        data = request.POST

        # user_image = request.FILES.get('signup_image')
        f_name = data.get('signup_f_name')
        l_name = data.get('signup_l_name')
        email_id = data.get('signup_email')
        dob = data.get('signup_DOB')
        # pwd = request.POST.get('signup_pwd')
        
        print(f_name)
        # print(user_image)
        print(dob)

        user  = user_details.objects.create(
            f_name = f_name , 
            l_name = l_name,
            email = email_id , 
            # user_image = user_image,
            pwd = "hello",
            dob = dob,
            mobile = 9307636852,
            role=1,
        )

        # user.set_password(pwd)

        # user = User.objects.filter(email = email)
        # if user.exists():
        #     messages.info(request, "email alreasdy exists")
        #     return redirect('/signup/')

        request.session['rd']=1
        return redirect('/login/')
    
    queryset = user_details.objects.all()
    if request.GET.get('search_user'):
        print(request.GET.get('search_user'))
        # queryset = queryset.filter(f_name__icontains = request.GET.get('search_user'))

    users = user_details.objects.all()
    context = {'users' : users}
    return render(request ,  'signup.html' , context)

def delete_user(request , email):
    print("hello")
    print(email)
    user = user_details.objects.get(email = email)
    print(user)
    user.delete()
    return redirect('/register')

def update_user(request , email):
    return redirect('/signup')


#sort in asceding order
#users = user_details.objects.all().order_by('dob')
#sort in descending order
#users = user_details.objects.all().order_by('-dob')

#slicing
#users = user_details.objects.all().order_by('dob')[0:200]

#__gte -> greater or equal __lte -> less than equal
#users = user_details.objects.filter(dob__gte = '10-04-2002')
#__startswith , __endswith , __icontains in filter

#foreign key tables
# queryset = course.objects.all()
# queryset[0].teacher_id.f_name   (queryset[0].teacher_id starts pointing to the table in which this foreign key is a primary key)

#queryset.count()
#queryset = course.objects.filter(type__in = l) where l=["Python" , "C++"]
#queryset = course.objects.exclude(type == "Python")

#queryset.values()
# similarly exists , distinct , reverse , values_list , none , union is the keyword

#get raises Exception filter don't

#aggregate functions -> work on single column like in sql sum avg max min
#annotate -> two or more columns
#result.objects.aggregate(Avg('marks'))
#result.objects.aggregate(Max('marks'))
#like group by
#result.object.values('marks').annotate(Count('marks'))





#for login

        # email = request.POST.get('login_email')
        # pwd = request.POST.get('login_pwd')

        # if not User.objects.filter(email = email).exists():
        #     messages.error(request , 'Invalid email')
        #     return redirect('/login/')

        # user = authenticate(email = email , password = pwd)
        
        # if user is None:
        #     messages.error(request , 'Invalid credentials')
        #     return redirect('/login/')
        # else:
        #     login(request , user)
        #     return redirect('/dashboard/')
        #to maintain session