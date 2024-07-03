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
from django.views.decorators.clickjacking import xframe_options_exempt


# Create your views here.

def home(request):
    return render(request , 'index.html')

def about(request):
    return render(request , 'about.html')

def services(request):
    return render(request , 'services.html')

def blog(request):
    return render(request , 'blog.html')

def faq(request):
    return render(request , 'faq.html')

def terms(request):
    return render(request , 'terms.html')

def privacy(request):
    return render(request , 'privacy.html')

@login_required(login_url='/login')
def show_full_result_teacher(request ,quiz_id):
    all_result = result.objects.filter(quiz_id=quiz_id)
    quiz_obj = quiz_desc.objects.get(pk=quiz_id)
    context = {'all_result' : all_result , 'quiz_obj':quiz_obj}
    return render(request , 'show_full_result_teacher.html' , context)

@login_required(login_url='/login')
def give_feedback(request , course_id):
    course_obj = course.objects.filter(course_id=course_id)[0]
    if request.method == 'POST':
        new_feedback_form = feedback_form(request.POST)
        
        if new_feedback_form.is_valid():
            feedback_text = new_feedback_form.cleaned_data['feedback_text']

            feedback_date = datetime.now()
            student_id = user_details.objects.get(pk= request.user.email)
            
            feedback_obj = feedback(user_id=student_id , feedback_date = feedback_date , feedback_text=feedback_text , course_id=course_obj)
            
            feedback_obj.save()
            return redirect(reverse('display_course_student' ,args=[course_id]))

    new_feedback_form =feedback_form()
    context={'course_obj' : course_obj , 'form':new_feedback_form}
    return render(request , 'give_feedback.html' , context)

@login_required(login_url='/login')
def show_full_result(request , result_id ):
    result_obj = result.objects.filter(result_id=result_id)[0]
    result_question_obj = result_question.objects.filter(result_id=result_id)
    course_id=0
    total_no_ques=0
    correctly_answered=0
    total_answered=0

    for ques in result_question_obj:
        total_no_ques+=1
        if ques.marked_option!=0:
            total_answered+=1
        if ques.marked_option==ques.question_id.correct_opt:
            correctly_answered+=1

    if result_obj:
        course_id=result_obj.quiz_id.course_id.course_id

    context= { 'result_obj' : result_obj , 'result_question_obj': result_question_obj , 
              'course_id' : course_id , 'total_no_ques':total_no_ques , 'correctly_answered':correctly_answered , 'total_answered':total_answered}
    return render(request , 'show_full_result.html' , context)

@login_required(login_url='/login')
def result_after_quiz(request , result_id , score,total_no_ques ,total_answered ,correctly_answered):
    # print(result_id)
    # print( ,  score,total_no_ques ,total_answered ,correctly_answered)
    context = {'result_id':result_id , 'score': score, 'total_no_ques': total_no_ques , 
               'total_answered':total_answered ,'correctly_answered':correctly_answered}
    # context={}
    return render(request , 'result_after_quiz.html' , context)

# @login_required(login_url='/login')
# def give_quiz(request , quiz_id):
#     all_ques = quiz_ques.objects.filter(quiz_id = quiz_id)
#     quiz_obj = quiz_desc.objects.filter(quiz_id=quiz_id)[0]
    
#     if request.method== 'POST':
        
#         result_id="2"
#         # result_id = quiz_id + "_" + str(datetime.now())
#         # print(request.user.email)
#         user=user_details.objects.get(email = request.user.email)
#         result_obj = result(quiz_id = quiz_obj, student_id =user , result_id=result_id , marks=0 , result_date=datetime.now() )
#         result_obj.save()
#         score=0
#         total_no_ques=len(all_ques)
#         total_answered=0
#         correctly_answered=0

#         for ques in all_ques:
#             answer_marked = request.POST.get(ques.ques_id)
#             marked_option = 0
#             if answer_marked == ques.opt1 :
#                 total_answered+=1
#                 marked_option=1
#                 if ques.correct_opt==1 :
#                     correctly_answered+=1
#                     score+=ques.ques_marks
#             elif answer_marked == ques.opt2 :
#                 total_answered+=1
#                 marked_option=2
#                 if ques.correct_opt==2 :
#                     correctly_answered+=1
#                     score+=ques.ques_marks
#             elif answer_marked == ques.opt3 :
#                 total_answered+=1
#                 marked_option=3
#                 if ques.correct_opt==3 :
#                     correctly_answered+=1
#                     score+=ques.ques_marks
#             elif answer_marked == ques.opt4 :
#                 total_answered+=1
#                 marked_option=4
#                 if ques.correct_opt==4 :
#                     correctly_answered+=1
#                     score+=ques.ques_marks

#             result_question_obj = result_question(question_id=ques ,  marked_option=marked_option, result_id=result_obj)
#             result_question_obj.save()
        
#         result.objects.filter(result_id="1").update(marks=score)

#         #change it to student dashboard
#         args=[]
#         return redirect(reverse('result_after_quiz' ,args=[result_id , score,total_no_ques ,total_answered ,correctly_answered]))


#     duration_seconds  = quiz_obj.quiz_duration.total_seconds()
#     context = {'all_ques' : all_ques , 'quiz_obj' : quiz_obj , 'duration_seconds' : duration_seconds}
#     return render(request , 'give_quiz.html' , context )

@login_required(login_url='/login')
def give_quiz(request , quiz_id):
    all_ques = quiz_ques.objects.filter(quiz_id = quiz_id)
    quiz_obj = quiz_desc.objects.filter(quiz_id=quiz_id)[0]
    
    total_no_ques=0
    correctly_answered=0
    total_answered=0

    if request.method== 'POST':
        
        # result_id="2"
        result_id = quiz_id + "_" + str(datetime.now())
        # print(request.user.email)
        # result_id="1"
        # result_id = quiz_id + "_" + str(datetime.now())
        print(request.user.email)
        user=user_details.objects.get(email = request.user.email)
        result_obj = result(quiz_id = quiz_obj, student_id =user , result_id=result_id , marks=0 , result_date=datetime.now() )
        result_obj.save()
        score=0

        for ques in all_ques:
            total_no_ques+=1
            answer_marked = request.POST.get(ques.ques_id)
            marked_option = 0
            if answer_marked == ques.opt1 :
                marked_option=1
                if ques.correct_opt==1 :
                    score+=ques.ques_marks
                    correctly_answered+=1
            elif answer_marked == ques.opt2 :
                marked_option=2
                if ques.correct_opt==2 :
                    score+=ques.ques_marks
                    correctly_answered+=1
            elif answer_marked == ques.opt3 :
                marked_option=3
                if ques.correct_opt==3 :
                    score+=ques.ques_marks
                    correctly_answered+=1
            elif answer_marked == ques.opt4 :
                marked_option=4
                if ques.correct_opt==4 :
                    score+=ques.ques_marks
                    correctly_answered+=1

            if marked_option!=0:
                total_answered+=1

            result_question_obj = result_question(question_id=ques ,  marked_option=marked_option, result_id=result_obj)
            result_question_obj.save()
        
        result.objects.filter(result_id=result_id).update(marks=score)

        return redirect(reverse('result_after_quiz' ,args=[result_id , score,total_no_ques ,total_answered ,correctly_answered]))
        result.objects.filter(result_id="1").update(marks=score)
        #change it to student dashboard
        return redirect('teacher_dashboard')


    duration_seconds  = quiz_obj.quiz_duration.total_seconds()
    context = {'all_ques' : all_ques , 'quiz_obj' : quiz_obj , 'duration_seconds' : duration_seconds}
    return render(request , 'give_quiz.html' , context )

@login_required(login_url='/login')
def update_ques(request , ques_id):
    ques_obj = quiz_ques.objects.filter(ques_id = ques_id)[0]
    quiz_id = ques_obj.quiz_id.quiz_id

    if request.method == 'POST':
        update_question_form = update_ques_form(request.POST)
        if update_question_form.is_valid():
            ques_text = update_question_form.cleaned_data['ques_text']
            opt1 = update_question_form.cleaned_data['opt1']
            opt2 = update_question_form.cleaned_data['opt2']
            opt3 = update_question_form.cleaned_data['opt3']
            opt4 = update_question_form.cleaned_data['opt4']
            correct_opt = update_question_form.cleaned_data['correct_opt']
            ques_marks = update_question_form.cleaned_data['ques_marks']

            ques_obj = quiz_ques(ques_text=ques_text , opt1=opt1 , opt2=opt2 , opt3=opt3 , 
                                opt4=opt4 , correct_opt=correct_opt, ques_marks=ques_marks ,
                                quiz_id=ques_obj.quiz_id , ques_id=ques_id)
            
            ques_obj.save()

            return redirect(reverse('display_quiz_teacher' ,args=[quiz_id]))
    
    
    update_question_form = update_ques_form()
    context = {'form' : update_question_form  , 'ques_obj' : ques_obj, 'quiz_detail':ques_obj.quiz_id}
    return render(request , 'update_ques.html' , context)

@login_required(login_url='/login')
def delete_ques(request , ques_id):
    ques_obj = quiz_ques.objects.filter(ques_id = ques_id)[0]
    quiz_id = ques_obj.quiz_id.quiz_id
    ques_obj.delete()
    quiz_desc.objects.filter(quiz_id=quiz_id).update(no_of_ques=ques_obj.quiz_id.no_of_ques-1)
    return redirect(reverse('display_quiz_teacher' ,args=[quiz_id]))

@login_required(login_url='/login')
def display_quiz_teacher(request , quiz_id):
    # print(quiz_id)
    all_ques = quiz_ques.objects.filter(quiz_id = quiz_id)
    # quizzes = quiz_desc.objects.all()
    quiz_desc.objects.filter(quiz_id=quiz_id+"?").update(quiz_id=quiz_id)
    quiz_obj = quiz_desc.objects.filter(quiz_id = quiz_id)
    # print(quiz_obj)
    # print(len(quiz_obj))
    
    context = {'all_ques' : all_ques , 'quiz_obj' : quiz_obj[0]}
    return render(request , 'display_quiz_teacher.html' , context)

@xframe_options_exempt
@login_required(login_url='/login')
def display_course_teacher(request , course_id):
    course_obj = course.objects.filter(course_id = course_id)
    all_quiz = quiz_desc.objects.filter(course_id = course_id)
    all_assignments = assignments.objects.filter(course_id = course_id)
    feedbacks = feedback.objects.filter(course_id = course_id)
    pdf_url = '/media/' + str(course_obj[0].course_pdf)
    pdf_urls = 'media/' + str(course_obj[0].course_pdf)
    url = '/static/' + str(course_obj[0].course_pdf)
    # print(pdf_url)
    # print(pdf_urls)
    context = {'all_quiz' : all_quiz , 'course_obj' : course_obj[0] , 'feedbacks' : feedbacks ,
                'pdf_url':pdf_url , 'pdf_urls':pdf_urls, 'url':url , 'all_assignments' : all_assignments,}
    # context = {'all_quiz' : all_quiz , 'course_obj' : course_obj[0]}
    return render(request , 'display_course_teacher.html' , context)

@login_required(login_url='/login')
def display_created_courses(request):
    all_courses = course.objects.filter(teacher_id = request.user.email)
    # print(all_courses)
    context = {'all_courses' : all_courses}
    return render(request , 'display_created_courses.html' , context)

@login_required(login_url='/login')
def teacher_dashboard(request):
    rd = request.session.get('rd')
    if rd==3:
        name = request.user.first_name + " " + request.user.last_name
        messages.info(request, f"You are now logged in as {name}.")
        request.session['rd']=0

    return render(request , 'teacher_dashboard.html')

# @login_required(login_url='/login')
# def set_ques(request  , quiz_id): 
#     if request.method == 'POST':
#         set_question_form = set_ques_form(request.POST)
#         if set_question_form.is_valid():
#             ques_text = set_question_form.cleaned_data['ques_text']
#             opt1 = set_question_form.cleaned_data['opt1']
#             opt2 = set_question_form.cleaned_data['opt2']
#             opt3 = set_question_form.cleaned_data['opt3']
#             opt4 = set_question_form.cleaned_data['opt4']
#             correct_opt = set_question_form.cleaned_data['correct_opt']
#             ques_marks = set_question_form.cleaned_data['ques_marks']

#             quiz_detail=quiz_desc.objects.get(pk=quiz_id)
#             ques_id=str(request.session['cnt'])+ "_" +str(quiz_id)

#             ques_obj = quiz_ques(ques_text=ques_text , opt1=opt1 , opt2=opt2 , opt3=opt3 , 
#                                 opt4=opt4 , correct_opt=correct_opt, ques_marks=ques_marks ,
#                                 quiz_id=quiz_detail , ques_id=ques_id)
            
#             ques_obj.save()
#             request.session['cnt']+=1
#             if(request.session['cnt'] == quiz_detail.no_of_ques):
#                 # request.session['cnt']=0
#                 return redirect('/teacher_dashboard')      
            
#     quiz_detail=quiz_desc.objects.get(pk=quiz_id)
#     set_question_form = set_ques_form()
#     context = {'form' : set_question_form  , 'ques_no':request.session['cnt'] , 'quiz_detail':quiz_detail}
#     return render(request , 'set_ques.html' , context)
@login_required(login_url='/login')
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
            
            ques_id=""
            try:
                if request.session['cnt']!=0:
                    ques_id=str(request.session['cnt'])+ "_" +str(quiz_id)
                else:
                    ques_id=str(quiz_detail.no_of_ques+1)+"_"+str(quiz_id)
            except:
                ques_id=str(quiz_detail.no_of_ques+1)+"_"+str(quiz_id)

            ques_obj = quiz_ques(ques_text=ques_text , opt1=opt1 , opt2=opt2 , opt3=opt3 , 
                                opt4=opt4 , correct_opt=correct_opt, ques_marks=ques_marks ,
                                quiz_id=quiz_detail , ques_id=ques_id)
            
            ques_obj.save()
            # request.session['cnt']+=1
            try :
                if request.session['cnt']!=0:
                    if request.session['cnt'] == quiz_detail.no_of_ques:
                        # request.session['create']=0
                        request.session['cnt']=0
                    
                        return redirect(reverse('display_course_teacher' ,args=[quiz_detail.course_id.course_id ]))
                    request.session['cnt']+=1
                else:
                    quiz_desc.objects.filter(quiz_id=quiz_id).update(no_of_ques=quiz_detail.no_of_ques+1)
                    return redirect(reverse('display_quiz_teacher' ,args=[quiz_id ]))    
            except :
                quiz_desc.objects.filter(quiz_id=quiz_id).update(no_of_ques=quiz_detail.no_of_ques+1)
                return redirect(reverse('display_quiz_teacher' ,args=[quiz_id ]))   
            
    quiz_detail=quiz_desc.objects.get(pk=quiz_id)
    set_question_form = set_ques_form()
    ques_no=0
    try: 
        if request.session['cnt']!=0:
            ques_no=request.session['cnt']
        else :
            ques_no=quiz_detail.no_of_ques+1
    except:
        ques_no=quiz_detail.no_of_ques+1
    context = {'form' : set_question_form  , 'ques_no':ques_no , 'quiz_detail':quiz_detail}
    return render(request , 'set_ques.html' , context)

@login_required(login_url='/login')
def create_quiz(request , course_id):
    if request.method =='POST':
        new_quiz_form = create_quiz_form(request.POST)

        if new_quiz_form.is_valid():
            quiz_title = new_quiz_form.cleaned_data['quiz_title']
            quiz_duration = new_quiz_form.cleaned_data['quiz_duration']
            no_of_ques = new_quiz_form.cleaned_data['no_of_ques']

            quiz_id = course_id+"_" + quiz_title + "_" + str(datetime.now())
            # quiz_id = 3
            course_id = course.objects.get(pk = course_id)

            quiz_obj = quiz_desc(quiz_title = quiz_title , quiz_duration = quiz_duration,
                                 no_of_ques = no_of_ques , quiz_id = quiz_id , course_id = course_id)
            
            quiz_obj.save()
            # request.session['cnt']=0
            request.session['cnt']=1
            return redirect(reverse('set_ques' ,args=[quiz_id ]))
        
    new_quiz_form = create_quiz_form()
    context = {'form' : new_quiz_form , 'course_id' : course_id}
    return render(request , 'create_quiz.html' , context)

@login_required(login_url='/login')
def upload_assignment(request , course_id):
    
    if request.method =='POST':
        new_quiz_form = assignment_form(request.POST , request.FILES)

        if new_quiz_form.is_valid():
            assignment_name = new_quiz_form.cleaned_data['assignment_name']
            assignment_desc = new_quiz_form.cleaned_data['assignment_desc']
            assignment_pdf = new_quiz_form.cleaned_data['assignment_pdf']
            assignment_duration = new_quiz_form.cleaned_data['assignment_duration']

            assignment_id = course_id+ "" + assignment_name + "" + str(datetime.now())
            course_id = course.objects.get(pk = course_id)

            assignment_obj = assignments(assignment_name = assignment_name , assignment_duration = assignment_duration,
                                 assignment_pdf = assignment_pdf , assignment_desc = assignment_desc , course_id = course_id,
                                 assignment_id = assignment_id)
            
            assignment_obj.save()
            return redirect(reverse('display_course_teacher' ,args=[assignment_obj.course_id.course_id ]))
        
    new_assignment_form = assignment_form()
    context = {'form' : new_assignment_form , 'course_id' : course_id}
    return render(request , 'upload_assignment.html' , context)

@login_required(login_url='/login')
def create_new_course(request):
    if request.method == 'POST':
        new_course_form = create_new_course_form(request.POST,request.FILES)
        
        if new_course_form.is_valid():
            course_name = new_course_form.cleaned_data['course_name']
            course_duration = new_course_form.cleaned_data['course_duration']
            category = new_course_form.cleaned_data['category']
            topic = new_course_form.cleaned_data['topic']
            course_material = new_course_form.cleaned_data['course_material']
            course_pdf = new_course_form.cleaned_data['course_pdf']

            publish_date = datetime.now()
            course_id = str(publish_date)+"_" + course_name
            # course_id = "3"
            teacher_id = user_details.objects.get(pk= request.user.email)
            
            course_obj = course(course_name= course_name , course_duration=course_duration , 
                                      category=category , topic=topic , course_material=course_material ,
                                      publish_date=publish_date , course_id=course_id , 
                                      teacher_id=teacher_id, course_pdf=course_pdf)
            
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
                elif request.user.role==2:
                    return redirect('/student_dashboard')
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




@login_required(login_url='/login')
def student_dashboard(request):
    rd = request.session.get('rd')
    if rd==3:
        name = request.user.first_name + " " + request.user.last_name
        messages.info(request, f"You are now logged in as {name}.")
        request.session['rd']=0

    all_courses = course.objects.all()
    all_enrollments = enrollment.objects.filter(student_id = request.user.email)
    enrolled_courses=[]
    for enrollments in all_enrollments:
        if enrollments.enrollment_status == "1":
            enrolled_courses.append(course.objects.filter(course_id=enrollments.course_id.course_id)[0])

    not_enrolled_courses=[]
    for courses in all_courses:
        flag=0
        for enrollments in all_enrollments:
            if enrollments.enrollment_status == "1":
                if enrollments.course_id.course_id == courses.course_id:
                    flag=1
                    break
        if flag == 0:
            not_enrolled_courses.append(courses)

    all_quizzes=[]
    for enrollments in enrolled_courses:
        quiz_set_with_specific_id=quiz_desc.objects.filter(course_id=enrollments.course_id)
        if len(quiz_set_with_specific_id) != 0:
            for quizzes in quiz_set_with_specific_id:
                all_quizzes.append(quizzes)

    pending_quizzes=[]

    all_results=[]

    for quizzes in all_quizzes:
        result_for_this_quiz = result.objects.filter(quiz_id=quizzes.quiz_id)
        if len(result_for_this_quiz) == 0:
            pending_quizzes.append(quizzes)
        else:
            for results in result_for_this_quiz:
                all_results.append(results)
    

    # print(all_quizzes)
    # print()
    # print(all_results)

    context= {'enrolled_courses' : enrolled_courses , 'not_enrolled_courses' : not_enrolled_courses , 'all_courses' : all_courses , 'pending_quizzes' : pending_quizzes , 'all_results' : all_results}
    return render(request , 'student_dashboard.html', context)

@xframe_options_exempt
@login_required(login_url='/login')
def display_course_student(request , course_id):
    # print(course_id)
    course_obj = course.objects.filter(course_id = course_id)
    if request.method == 'POST':
        new_feedback_form = feedback_form(request.POST)
        
        if new_feedback_form.is_valid():
            feedback_text = new_feedback_form.cleaned_data['feedback_text']

            feedback_date = datetime.now()
            student_id = user_details.objects.get(pk= request.user.email)
            
            feedback_obj = feedback(user_id=student_id , feedback_date = feedback_date , feedback_text=feedback_text , course_id=course_obj[0])
            
            feedback_obj.save()
            return redirect(reverse('display_course_student' ,args=[course_id]))

    new_feedback_form =feedback_form()
    feedbacks = feedback.objects.filter(course_id=course_id)
    all_quiz = quiz_desc.objects.filter(course_id = course_id)
    quiz_remaining =[]
    given_quiz_result=[]
    for quiz in all_quiz:
        if result.objects.filter(quiz_id = quiz.quiz_id , student_id=request.user.email):
            given_quiz_result.append(result.objects.filter(quiz_id = quiz.quiz_id , student_id=request.user.email)[0])
        else:
            quiz_remaining.append(quiz)
    # print(course_obj)
    # print(course_obj[0])
    pdf_url = '/media/' + str(course_obj[0].course_pdf)
    pdf_urls = 'media/' + str(course_obj[0].course_pdf)
    url = '/static/' + str(course_obj[0].course_pdf)
    # print(pdf_url)
    # print(pdf_urls)
    all_assignments = assignments.objects.filter(course_id = course_id)
    context = {'all_quiz' : all_quiz , 'course_obj' : course_obj[0] , 'feedbacks' : feedbacks ,
                'pdf_url':pdf_url , 'pdf_urls':pdf_urls, 'url':url , 'form':new_feedback_form , 
                'quiz_remaining' : quiz_remaining , 'given_quiz_result':given_quiz_result , 'all_assignments':all_assignments}
    return render(request , 'display_course_student.html' , context)

@login_required(login_url='/login')
def enroll(request , course_id):
    course_obj = course.objects.filter(course_id=course_id) 
    enrollment_id = course_id + " " + str(request.user.email)
    enrollment_date = datetime.now()
    enrollment_status = "1"

    enroll_obj = enrollment(course_id = course_obj[0], student_id = user_details.objects.filter(email=request.user.email)[0] , enrollment_id = enrollment_id,
                            enrollment_date = enrollment_date , enrollment_status = enrollment_status)
    
    enroll_obj.save()
    return redirect('student_dashboard')









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