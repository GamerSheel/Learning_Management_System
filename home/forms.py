from django import forms
from .models import *

class user_detail_forms(forms.ModelForm):
    class Meta:
        model = user_details
        fields = ['first_name' , 'last_name' , 'email' , 'password' , 'dob' , 'address' ,
                  'mobile' , 'role' , 'institute' , 'role_desc']

class login_user_form(forms.Form):
    email = forms.EmailField(label = "Email Id" , widget=forms.EmailInput(attrs={'class' : "form-control"}))
    password = forms.CharField(label = "Password" , widget=forms.PasswordInput(attrs={'class' : "form-control"}))

    fields =['__all__']

class create_new_course_form(forms.ModelForm):
    class Meta:
        model = course
        fields = ['course_name' , 'course_duration' , 'category' , 'topic' , 'course_material']

class create_quiz_form(forms.ModelForm):
    class Meta:
        model = quiz_desc
        fields = ['quiz_title' , 'quiz_duration' , 'no_of_ques']

class set_ques_form(forms.ModelForm):
    class Meta:
        model = quiz_ques
        fields = [ 'ques_text' , 'opt1' , 'opt2', 'opt3', 'opt4', 'correct_opt' , 'ques_marks']

# class user_detail_forms(forms.Form):
#     First_Name = forms.CharField(label = "First Name")
#     Last_Name = forms.CharField(label = "Last Name" , required=False, widget=forms.TextInput(attrs={'class' : "form-control"}))


# class MyModelForm(forms.ModelForm):
#     extra_field = forms.CharField(max_length=100, label='Extra Field')

#     class Meta:
#         model = MyModel
#         fields = ['name', 'age', 'extra_field']