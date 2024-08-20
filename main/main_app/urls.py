from django.urls import path
from . import views

urlpatterns = [
    path('company_home/',views.company_home,name='company_home'),
    path('emp_home/',views.emp_home,name='emp_home'),
    path('admin_panel/',views.admin_panel,name='admin_panel'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('job_create/',views.job_create,name='job_create'),
    path('add_profile/',views.profilecreate,name='add_profile'),
    path('com_det/<int:id>/',views.company_det,name='company_det'),

    
    path('forgotpassword/',views.forgot_password,name='forgot_password'),
    path('verfy_otp/<int:id>/',views.otp_verify,name='otp_verify'),
    path('passwordreset/<int:id>/',views.password_reset,name='password_reset'),

    path('com_pro/',views.com_pro,name='com_pro'),

    path('apply/<int:id>/',views.apply_fun,name='applay'),

    path('emp_pro/',views.emp_profile,name='emp_pro'),
    path('companyview_pro/',views.company_profile,name='company_pro'),

    path('history',views.history,name='job_his'),
    path('dashcom/',views.dash_com,name='dash_com'),

    path('com_seek_pro/<int:id>/',views.com_seek_pro,name='com_seek_pro'),

    path('select/<int:id>/',views.select,name='select'),
    path('reject/<int:id>/',views.reject,name='reject'),

    path('deactivate_job/<int:id>/', views.deactivate_job, name='deactivate_job'),
    path('activate_job/<int:id>/', views.activate_job, name='activate_job'),

    path('ad_com/<int:id>/',views.ad_com,name='ad_com'),
    path('ad_emp/<int:id>/',views.ad_emp,name='ad_emp'),

    path('inactive/',views.acc_in,name='account_inactive'),
    path('approve/<int:id>/',views.approve_user,name='approve'),
    path('remove/<int:id>/',views.remove_user,name='remove'),


    path('edit_profile/', views.edit_profile, name='pro_edit_emp'),
    path('edit_profile_com/', views.edit_pro_com, name='edit_pro_com'),

    path('edit_job/<int:id>/',views.edit_job,name='edit_job'),
    path('',views.not_login,name='not_login'),

]