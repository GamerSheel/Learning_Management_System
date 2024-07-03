from django.db import models
from django.contrib.auth.models import User , AbstractUser , AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from datetime import timedelta

# Create your models here.

#role 1 -> Teacher
#role 2 -> Student



class UserManager(BaseUserManager):
    def create_user(self , email , password=None , **extra_fields):
        if not email:
            raise ValueError("Email Id is required")
        
        user = self.model( email_id=self.normalize_email(email) , **extra_fields)
        # Normalizes email addresses by lowercasing the domain portion of the email address.

        user.set_password(password)
        print("in models.py in UserManager")
        print(password)
        user.save(using = self.db)
        return user

    def create_superuser(self , username , password, **kwargs):
        user = self.model(email=username , is_staff=True , is_superuser=True , **kwargs)
        user.set_password(password)
        user.save()
        return user

class user_details(AbstractUser):
    username=None
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True , primary_key=True)

    dob = models.DateField()
    address = models.TextField()
    mobile = models.CharField(max_length=10)
    role = models.IntegerField()
    institute = models.CharField(max_length=200)
    role_desc = models.TextField()
    # user_image = models.ImageField(upload_to="static/user_image")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# class user_details(models.Model):
#     f_name = models.CharField(max_length=100)
#     l_name = models.CharField(max_length=100)
#     dob = models.DateField()
#     email = models.EmailField(primary_key=True)
#     address = models.TextField()
#     # user_image = models.ImageField(upload_to="static/user_image")
#     mobile = models.CharField(max_length=10)
#     role = models.IntegerField()
#     institute = models.CharField(max_length=200)
#     role_desc = models.TextField()
#     pwd = models.CharField(max_length=200)
#     # file = models.FileField()


class course(models.Model):
    course_id = models.CharField(max_length=100 ,primary_key=True)
    teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    publish_date = models.DateTimeField()
    course_duration = models.DurationField()
    category = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    course_material = models.TextField()
    course_pdf = models.FileField(upload_to='static/pdfs/' ,  default='static/pdfs/default_pdf.pdf')

    # for sorting records in table in database
    # class Meta:
    #     ordering = ['topic']


class quiz_desc(models.Model):
    quiz_id = models.CharField(max_length = 100 , primary_key=True)
    course_id = models.ForeignKey(course , on_delete=models.CASCADE)
    quiz_title = models.CharField(max_length=100)
    quiz_duration = models.DurationField()
    no_of_ques = models.IntegerField()
    #quiz_status = models.CharField()

class quiz_ques(models.Model):
    ques_id = models.CharField(max_length=100 , primary_key=True)
    quiz_id = models.ForeignKey(quiz_desc , on_delete=models.CASCADE)
    ques_text = models.TextField()
    opt1 = models.CharField(max_length=200)
    opt2 = models.CharField(max_length=200)
    opt3 = models.CharField(max_length=200)
    opt4 = models.CharField(max_length=200)
    correct_opt = models.IntegerField()
    ques_marks = models.IntegerField()

class feedback(models.Model):
    user_id = models.ForeignKey(user_details , on_delete=models.CASCADE)
    feedback_date = models.DateTimeField(primary_key=True)
    feedback_text = models.TextField()
    course_id = models.ForeignKey(course , on_delete= models.CASCADE)

# enrollment and result ques
class enrollment(models.Model):
    course_id = models.ForeignKey(course , on_delete=models.CASCADE)
    student_id = models.ForeignKey(user_details , on_delete=models.CASCADE)
    enrollment_id = models.CharField(max_length=200,primary_key=True)
    enrollment_date = models.DateTimeField()
    enrollment_status = models.CharField(max_length=200)

class result(models.Model):
    quiz_id = models.ForeignKey(quiz_desc , on_delete=models.CASCADE)
    student_id = models.ForeignKey(user_details , on_delete=models.CASCADE)
    result_id = models.CharField(max_length=250 , primary_key=True)
    marks = models.IntegerField()
    result_date = models.DateTimeField()

class result_question(models.Model):
    class Meta:
        unique_together = (('question_id','result_id'),)
    question_id = models.ForeignKey(quiz_ques , on_delete=models.CASCADE)
    marked_option = models.IntegerField()
    result_id = models.ForeignKey(result , on_delete=models.CASCADE)
    
class assignments(models.Model):
    assignment_id = models.CharField(max_length=200,primary_key=True)
    assignment_name = models.TextField()
    assignment_desc = models.TextField()
    course_id = models.ForeignKey(course , on_delete=models.CASCADE)
    assignment_pdf = models.FileField(upload_to='static/pdfs/' ,  default='static/pdfs/default_pdf.pdf')
    default_duration = timedelta(hours=1)  # Default duration of 1 hour
    assignment_duration = models.DurationField(default=default_duration)


