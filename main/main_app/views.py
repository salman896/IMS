from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST.get('Name')
        email = request.POST.get('Email')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')
        role = request.POST.get('role')
        if password1 == password2:
            user = CustomUser.objects.create_user(username=username,email=email,password=password1,role=role)
            user.save()
            
            return redirect('login')
        
        return redirect('/')
    filter_ROLE_CHOICE = [(id,name) for id,name in ROLE_CHOICE if name != 'Admin']
    context = {'role_choices':filter_ROLE_CHOICE}
    return render(request,'register.html',context)


def company_home(request): 
    main = Add_job.objects.filter(company=request.user)
    context = {'main':main}  

    return render(request,'company_home.html',context)

# def emp_home(request):  
#     if request.method == 'POST':
#         search = request.POST.get('search')
#         main = Add_job.objects.filter(Q(job__contains=search) | Q(salary = search) | Q ())
#     # ma = CustomUser.objects.all()
#     else:
#         main = Add_job.objects.all()
#     context = {'main':main}  

#     return render(request,'emp_home.html',context)


def emp_home(request):
    if request.method == 'POST':
        search_query = request.POST.get('search')
        main = Add_job.objects.filter(
            Q(job__icontains=search_query) | 
            Q(salary__icontains=search_query) | 
            Q(company__username__icontains=search_query)
        )
    else:
        main = Add_job.objects.all()
    context = {'main': main}
    return render(request, 'emp_home.html', context)

def not_login(request):  
    ma = CustomUser.objects.all()
    main = Add_job.objects.all()
    context = {'main':main,'ma':ma}  

    return render(request,'not_login.html',context)

def admin_panel(request):  
    main = CustomUser.objects.all()
    context ={'main':main}
    return render(request,'admin_panel.html',context)  

    return render(request,'admin_panel.html')

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            
            if user.is_approved == True or user.role == 1:  # Check if user account is active
                login(request, user)
                if user.role == 1:
                    return redirect('admin_panel')
                elif user.role == 2:
                    if com_profile.objects.filter(com_user=user).exists():
                        return redirect('company_home')
                    else:
                        return redirect('com_pro')
                elif user.role == 3:
                    if Add_profile.objects.filter(emp=user).exists():
                        return redirect('emp_home')
                    else:
                        return redirect('add_profile')
            else:
                # Redirect to a page indicating that the account is not active
                return redirect('account_inactive')
        else:
            return redirect('register')  # User authentication failed
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')
# company job create

# def job_create(request):
#     if request.method == 'POST':
#         job = request.POST.get('job')
#         details = request.POST.get('details')
        
#         salary = request.POST.get('salary')
#         location = request.POST.get('location')
#         description = request.POST.get('description')
#         education = request.POST.getlist('education')
#         skill = request.POST.getlist('skills')

#         education1 = ','.join(education)
#         skills = ','.join(skill)

#         main = Add_job.objects.create(company=request.user,job=job,details=details,salary=salary,location=location,description=description,education=education1,skill=skills)
#         main.save()
#         return redirect('company_home')
#     return render(request,'job_create.html')



def job_create(request):
    if request.method == 'POST':
        job = request.POST.get('job')
        details = request.POST.get('details')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        description = request.POST.get('description')
        education = request.POST.getlist('education')
        skill = request.POST.getlist('skills')

        education1 = ','.join(education)
        skills = ','.join(skill)

        main = Add_job.objects.create(
            company=request.user,
            job=job,
            details=details,
            salary=salary,
            location=location,
            description=description,
            education=education1,
            skill=skills
        )

        # Fetch all employees with role=3 (Employee)
        employees = get_user_model().objects.filter(role=3)

        # Send email notification to each employee
        for employee in employees:
            subject = 'New Job Opening'
            message = render_to_string('notification_email.html', {
                'company': request.user.username,
                'job': job
            })
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'your_email@example.com', [employee.email], html_message=message)

        return redirect('company_home')
    
    return render(request,'job_create.html')

def company_det(request,id):
    
    main = Add_job.objects.get(id=id)
    edu = main.education.split(',')
    skill = main.skill.split(',')

    applied = Applay_job.objects.filter(job_det=main, emp=request.user).exists()

    context = {'main':main,'applied':applied,'edu':edu,'skill':skill}
    return render(request,'company_det.html',context)



def profilecreate(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile_number = request.POST.get('mobile_number')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        cv_file = request.FILES.get('cv')
        image_file = request.FILES.get('image')
        
        # Get education and skills
        education = request.POST.getlist('education')
        skills = request.POST.getlist('skills')

        # Join multiple values into a single string separated by comma
        education_str = ','.join(education)
        skills_str = ','.join(skills)

        profile = Add_profile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            mob=mobile_number,
            date_of_birth=date_of_birth,
            gender=gender,
            cv=cv_file,
            image=image_file,
            emp=request.user,
            education=education_str,
            skill=skills_str
        )
        profile.save()

        return redirect('emp_home')

    return render(request, 'profile_create.html')


def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username=username).first()
        if user:
            email = user.email
            otp = random.randrange(1000,9999)
            subject = 'Password Reset'
            message = f'Here is your otp - {otp}'
            from_email = 'salmanap007009@gmail.com'
            to = [email]
            send_mail(
                subject = subject,
                message = message,
                from_email =from_email,
                recipient_list = to,
                fail_silently = False
            )
            UserOTP.objects.update_or_create(
            user=user,
            defaults = {'otp':otp}
            )
            return redirect('otp_verify',user.id)
           
    return render(request,'forgot_password.html')

def otp_verify(request,id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        user_otp_obj = UserOTP.objects.filter(user=user).first()
        send_otp = user_otp_obj.otp
        if submitted_otp == send_otp:
            messages.success(request, 'OTP Verified')
            return redirect('password_reset',user.id)
        messages.error(request, 'Please enter valid OTP')
        return redirect('otp_verify',id)
    
    return render(request,'otp_verify.html',context={'email':user.email})


def password_reset(request,id):
    user = CustomUser.objects.get(id=id)
    if request.method == "POST":
        password1=request.POST.get('password1') 
        password2=request.POST.get('password2')
        if password2 == password1:
            user.set_password(password2)
            user.save()
            return redirect('login') 
        
    return render(request,"password_reset.html")   

def com_pro(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        address = request.POST.get('address')
        details = request.POST.get('details')
        image = request.FILES.get('image')

        # Assuming request.user is the currently logged-in user
        main = com_profile.objects.create(
            company=company,
            email=email,
            mob=mob,
            address=address,
            details=details,
            com_user=request.user,
            image=image
        )
        main.save()
        return redirect('company_home') 

    return render(request, 'com_pro.html')

def apply_fun(request,id):
    job = Add_job.objects.get(id=id)
    if Applay_job.objects.filter(job_det=job,emp = request.user).exists():
        return redirect('company_det', id=id)
    else:
        main = Applay_job.objects.create(applay=True,job_det=job,emp=request.user)
        main.save()
        return redirect('company_det', id=id)

#emp profile


def emp_profile(request):
    main = get_object_or_404(Add_profile, emp=request.user)
    edu = main.education.split(',')
    skill = main.skill.split(',')
    context = {'main':main,'edu':edu,'skill':skill}
    return render(request,'emp_pro.html',context)

def company_profile(request):
    main = get_object_or_404(com_profile, com_user=request.user)
    context = {'profile':main}
    return render(request,'com_pro_view.html',context)

#applay 

def history(request):
    main = Applay_job.objects.filter(emp = request.user)
    context = {'main':main}
    return render(request,'history.html',context)

def dash_com(request):
    
    main = Applay_job.objects.filter(job_det__company = request.user)
    


    context = {'main':main}
    return render(request,'dashbord_com.html',context)

def com_seek_pro(request,id):
    sub = Applay_job.objects.get(id=id)
    sub.view = True
    sub.save()
    
    main = Add_profile.objects.filter(emp = sub.emp)
    context = {'main':main}
    return render(request,'seek_pro.html',context)



# def select(request,id):
#     main = Applay_job.objects.get(id=id)
#     main.select = True
#     main.save()
#     return redirect('dash_com')

def select(request, id):
    main = Applay_job.objects.get(id=id)
    main.select = True
    main.save()

    # Send email notification to the employee
    subject = 'You have been selected for a job'
    message = 'Congratulations! You have been selected for the job. Please contact the employer for further details.'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [main.emp.email]  # Assuming CustomUser has an email field

    send_mail(subject, message, from_email, to_email, fail_silently=False)

    return redirect('dash_com')

def reject(request,id):
    main = Applay_job.objects.get(id=id)
    main.select = False
    main.save()
    return redirect('dash_com')

def deactivate_job(request, id):
    job = Add_job.objects.get(id=id)
    job.is_active = False
    job.save()
    return redirect('company_det', id=id)

def activate_job(request, id):
    job = Add_job.objects.get(id=id)
    job.is_active = True
    job.save()
    return redirect('company_det',id = id)


def ad_com(request,id):
    main = CustomUser.objects.get(id=id)
    context = {'main':main}
    return render(request,'ad_com.html',context)

def ad_emp(request,id):
    main = CustomUser.objects.get(id=id)
    context = {'main':main}
    return render(request,'ad_emp.html',context)

def acc_in(request):

    return render(request,'inactive.html')

def approve_user(request,id):
    main = CustomUser.objects.get(id=id)
    main.is_approved = True
    main.save()
    return redirect('admin_panel')

def remove_user(request,id):
    main = CustomUser.objects.get(id=id)
    
    main.delete()
    return redirect('admin_panel')

# def edit_profile(request):
#     main = Add_profile.objects.get(emp=request.user)
    
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')
#         mob = request.POST.get('mob')
#         address = request.POST.get('address')
#         date_of_birth = request.POST.get('date_of_birth')
#         gender = request.POST.get('gender')
#         cv_file = request.FILES.get('cv')
#         image_file = request.FILES.get('image')
#         # Assuming you have ForeignKey fields as well

#         main.first_name = first_name
#         main.last_name = last_name
#         main.email = email
#         main.mob = mob
#         main.address = address
#         if date_of_birth:
#             main.date_of_birth = date_of_birth
#         if image_file:
#             main.image=image_file
#         if cv_file:
#             main.cv=cv_file
#         main.gender= gender
#         main.emp = request.user

#         main.save()
        
#         return redirect('emp_home')
#     context = {'profile':main,'cho':Add_profile.gen_choice}
#     return render(request,'pro_edit_emp.html',context)

def edit_profile(request):
    main = Add_profile.objects.get(emp=request.user)
    
    if request.method == 'POST':

        edu = request.POST.getlist('education')
        skills = request.POST.getlist('skills')

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mob = request.POST.get('mobile_number')  # Assuming 'mobile_number' field in the form
        address = request.POST.get('address')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        cv_file = request.FILES.get('cv')
        image_file = request.FILES.get('image')
        
        education1 = ','.join(edu)
        skill1 = ','.join(skills)

        # Update profile fields
        main.first_name = first_name
        main.last_name = last_name
        main.email = email
        main.mob = mob
        main.address = address
        if date_of_birth:
            main.date_of_birth = date_of_birth
        main.gender = gender

        # Update CV and image if provided
        if cv_file:
            main.cv = cv_file
        if image_file:
            main.image = image_file
        if education1:
            main.education = education1
        if skill1:
            main.skill = skill1
        

        main.save()
        
        return redirect('emp_home')
    
    context = {'profile': main, 'cho': Add_profile.gen_choice}
    return render(request, 'pro_edit_emp.html', context)

def edit_pro_com(request):
    main = com_profile.objects.get(com_user=request.user)
    
    if request.method == 'POST':
        company = request.POST.get('company')
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        address = request.POST.get('address')
        details = request.POST.get('details')
        image = request.FILES.get('image')
        # Assuming you have ForeignKey fields as well

        main.company = company
        main.email = email
        main.mob = mob
        main.address = address
        main.details = details
        main.com_user = request.user 
        if image:
            main.image = image
         # Assuming com_user is a ForeignKey to CustomUser

        main.save()
        
        return redirect('company_home')  # Redirect to appropriate URL after saving
    context = {'profile': main}
    return render(request, 'pro_edit_com.html', context)


def edit_job(request,id):
    main = Add_job.objects.get(id=id)
    
    if request.method == 'POST':
        job = request.POST.get('job')
        details = request.POST.get('details')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        description = request.POST.get('description')
        skill = request.POST.getlist('skills')
        education = request.POST.getlist('education')
        # Assuming you have ForeignKey fields as well
        # Assuming the ForeignKey field is 'company'
        edu = ','.join(education)
        skills = ','.join(skill)


        main.job = job
        main.details = details
        main.salary =salary
        main.location = location
        main.description = description
        main.skill = skills
        main.education = edu
        main.company = request.user
        main.save()
        return redirect('company_det', id=id)  # Redirect to detail view after editing
    
    context = {'job': main}
    return render(request, 'edit_job.html', context)
