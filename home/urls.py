from django.urls import path
from home import views

urlpatterns = [
    path('', views.home , name="home" ),
    path('register/' , views.register , name="register"),
    path('signup/' , views.signup , name="signup"),
    path('delete_user/<email>/' , views.delete_user ,  name="delete_user"),
    path('login/' , views.login_page , name="login_page"),
    path('dashboard/' , views.dashboard , name="dashboard"),
    path('logout/' , views.logout_page , name="logout_page"),
    path('create_new_course/' , views.create_new_course , name="create_new_course"),
    path('create_quiz/<str:course_id>/' , views.create_quiz , name="create_quiz"),
    path('set_ques/<str:quiz_id>' , views.set_ques , name="set_ques"),
    path('teacher_dashboard/' , views.teacher_dashboard , name="teacher_dashboard"),
    path('display_created_courses/' , views.display_created_courses , name="display_created_courses"),
    path('display_course_teacher/<str:course_id>/' , views.display_course_teacher , name="display_course_teacher"),
    path('display_quiz_teacher/<str:quiz_id>/' , views.display_quiz_teacher , name="display_quiz_teacher"),
    path('delete_ques/<str:ques_id>/' , views.delete_ques , name="delete_ques"),
    path('update_ques/<str:ques_id>/' , views.update_ques , name="update_ques"),
    path('give_quiz/<str:quiz_id>/' , views.give_quiz , name="give_quiz")
    path('student_dashboard/' , views.student_dashboard, name="student_dashboard"),
    path('enroll/<str:course_id>' , views.enroll , name = "enroll"),
<<<<<<< HEAD
    path('result_after_quiz/<str:result_id>/<int:score>/<int:total_no_ques>/<int:total_answered>/<int:correctly_answered>/' , views.result_after_quiz , name = "result_after_quiz"),
    path('show_full_result/<str:result_id>/' , views.show_full_result , name="show_full_result"),
    path('give_feedback/<str:course_id>/'  ,views.give_feedback , name="give_feedback"),
    path('show_full_result_teacher/<str:quiz_id>/'  ,views.show_full_result_teacher , name="show_full_result_teacher"),
    path('display_course_student/<str:course_id>/' , views.display_course_student , name="display_course_student"),
    path('about/' , views.about , name="about"),
    path('services/' , views.services , name="services"),
    path('blog/' , views.blog , name="blog"),
    path('faq/' , views.faq , name="faq"),
    path('terms/' , views.terms , name="terms"),
    path('privacy/' , views.privacy , name="privacy"),
=======

>>>>>>> parent of 91f126e (Feedback)
]
