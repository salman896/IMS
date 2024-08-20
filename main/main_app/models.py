
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models 



class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extrafields):
        if not username:
            raise ValueError('User must have a username')
        if not password:
            raise ValueError('User must have a password') 
        user=self.model(username=username,**extrafields)
        user.set_password(password)
        user.save()
        return user 

    def create_superuser(self,username,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        extra_fields.setdefault('role',1)
        return self.create_user(username, password ,**extra_fields)


ROLE_CHOICE=[
    (1,'Admin'),
    (2,'Company'),
    (3,'Employee')
]

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=100,unique=True)
    email=models.EmailField(blank=True,null=True)
    is_active=models.BooleanField(default=True,verbose_name='active')
    is_staff=models.BooleanField(default=False)
    role=models.IntegerField(choices=ROLE_CHOICE,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()

    def __str__(self):
        return self.username
    

# company job creation

class Add_job(models.Model):

    job = models.CharField(max_length=30,null=True)
    details = models.TextField(null=True)
    salary = models.CharField(max_length=20,null=True)
    location = models.CharField(max_length=20,null=True)
    description =models.TextField(null=True)
    skill = models.CharField(max_length=39,null=True)
    education = models.CharField(max_length=20,null=True)
    company = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True,null=True)

    def __str__(self):
        return self.job

# emp profile creation


class Add_profile(models.Model):

    gen_choice = (('Male','Male'),
                  ('Female','Female'),
                  ('Other','Other'))

    first_name = models.CharField(max_length=20,null=True)
    last_name = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    mob = models.IntegerField(null=True)
    address = models.CharField(max_length=100,null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=20,choices=gen_choice,default="Male",null=True)
    education = models.CharField(max_length=30,null=True)
    skill = models.CharField(max_length=20,null=True)
    emp = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    cv = models.FileField(upload_to='cv/', null=True)
    image = models.ImageField(upload_to='images/', null=True)


    def __str__(self):
        return self.first_name
    
    
class UserOTP(models.Model):
    otp = models.CharField(max_length=5)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class com_profile(models.Model):

    image = models.ImageField(upload_to='images2/',null=True)
    company = models.CharField(max_length=20,null=True)
    email = models.EmailField(max_length=30,null=True)
    mob = models.IntegerField(null=True)
    address = models.CharField(max_length=100,null=True)
    details = models.TextField(null=True)
    com_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.company
    

class Applay_job(models.Model):

    applay = models.BooleanField(default=False,null=True)
    job_det = models.ForeignKey(Add_job,on_delete=models.CASCADE,null=True)
    select = models.BooleanField(default=None,null=True)
    view = models.BooleanField(default=False,null=True)
    emp = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)

    
