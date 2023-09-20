from django.urls import path, include
from medicapp import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from medicapp.views import PatientListView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot/', views.forgot, name='forgot'),
    path('patient/', views.patient_home, name='patient'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/', include('allauth.urls')),  
    path('login/', include('allauth.socialaccount.urls')), 
    path('create_profile/', views.create_profile, name='create_profile'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('diagnosis/', views.diagnosis, name='diagnosis'),
    path('diagnosis/predict', views.MakePrediction, name='predict'),
    path('result/', views.patient_result, name='result'),
    path('result/ment', views.MakeAppointment, name='ment'),
    path('ment', views.patient_appointment, name='ment_list'),
    path('doctor/', views.doctor_home, name='doctor'),
    path('recommend/', views.doctor_recommend, name='recommend'),
    path('recommend/predict', views.MakeMend, name='mend'),
    path('meet', views.doctor_ment, name='meet_list'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('patientinfo/', PatientListView.as_view(), name='patientinfo'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    path('doctor_info/', views.doctor_info, name='doctor_info'),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('home/', views.home, name='home'),  
    path('view_patient_info/', views.view_patient_info, name='view_patient_info'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),

    



    # PASSWORD RESET
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
