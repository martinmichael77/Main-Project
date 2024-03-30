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
    # path('ment', views.patient_appointment, name='ment_list'),
    path('doctor/', views.doctor_home, name='doctor'),
    path('recommend/', views.doctor_recommend, name='recommend'),
    path('recommend/predict', views.MakeMend, name='mend'),
    # path('meet', views.doctor_ment, name='meet_list'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('patientinfo/', PatientListView.as_view(), name='patientinfo'),
    path('add_doctor', views.add_doctor, name='add_doctor'),
    # path('appointment_success', views.appointment_success, name='appointment_success'),
    path('doctor_info/', views.doctor_info, name='doctor_info'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('home/', views.home, name='home'),  
    path('view_patient_info/', views.view_patient_info, name='view_patient_info'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('activate_doctor/<int:doctor_id>/', views.activate_doctor, name='activate_doctor'),
    path('deactivate_doctor/<int:doctor_id>/', views.deactivate_doctor, name='deactivate_doctor'),
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('confirm_appointment_doctor/<int:appointment_id>/', views.confirm_appointment_doctor, name='confirm_appointment_doctor'),
    path('complete_appointment_doctor/<int:appointment_id>/', views.complete_appointment_doctor, name='complete_appointment_doctor'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('appointments/', views.list_appointments, name='appointments'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    # path('paymenthandler/payment_success/', views.payment_success, name='payment_success'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('medical_report/', views.medical_report, name='medical_report'),
    # path('generate_pdf/<int:medical_record_id>/', views.generate_pdf, name='generate_pdf'),
    path('generate_pdf/<int:medical_record_id>/', views.generate_pdf, name='generate_pdf'),
    path('payment_success/', views.payment_success, name='payment_success'),
    # path('api/data/', views.chart_data, name='chart_data'),



    path('monthly_appointment_counts/', views.monthly_appointment_counts, name='monthly_appointment_counts'),
    # path('payment_status_pie_chart/', views.payment_status_pie_chart, name='payment_status_pie_chart'),
    path('refill_request_view/<str:username>/', views.refill_request_view, name='refill_request_view'),
    path('qrscan/<int:appointment_id>/', views.qrscan, name='qrscan'),
    path('add_counselor/', views.add_counselor, name='add_counselor'),
    path('counselorinfo', views.counselor_list, name='counselorinfo'),
    path('login_counselor/', views.login_counselor, name='login_counselor'),
    path('base_counselor', views.base_counselor, name='base_counselor'),
    path('home_counselor', views.home_counselor, name='home_counselor'),
    path('patient_counselling', views.patient_counselling, name='patient_counselling'),
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    path('nearby_hospital', views.nearby_hospital, name='nearby_hospital'),
    path('view_hospital', views.view_hospital, name='view_hospital'),
    path('counselor_appointment', views.counselor_appointment, name='counselor_appointment'),
    path('counselor_appointments', views.counselor_appointments, name='counselor_appointments'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('counselor/feedback/', views.counselor_feedback, name='counselor_feedback'),
    path('counselor_list', views.counselor_list, name='counselor_list'),
    path('activate_counselor/<int:counselor_id>/', views.activate_counselor, name='activate_counselor'),
    path('counselors/deactivate/<int:counselor_id>/', views.deactivate_counselor, name='deactivate_counselor'),
    path('counselor_appointments_list', views.counselor_appointments_list, name='counselor_appointments_list'),    
    path('add_healthcare_tip', views.add_healthcare_tip, name='add_healthcare_tip'),
    path('view_healthcare_tips', views.view_healthcare_tips, name='view_healthcare_tips'),
    path('like_tip/<int:tip_id>/', views.like_tip, name='like_tip'),
    path('share_tip/<int:tip_id>/', views.share_tip, name='share_tip'),
    path('bookmark_tip/<int:tip_id>/', views.bookmark_tip, name='bookmark_tip'),
    path('view_healthcare_tips_admin', views.view_healthcare_tips_admin, name='view_healthcare_tips_admin'),
    path('edit_healthcare_tip/<int:tip_id>/', views.edit_healthcare_tip, name='edit_healthcare_tip'),
    path('delete_healthcare_tip/<int:tip_id>/', views.delete_healthcare_tip, name='delete_healthcare_tip'),
    # path('health_tracker_home', views.health_tracker_home, name='health_tracker_home'),
    # path('record_health_metric/', views.record_health_metric, name='record_health_metric'),
    # path('view_health_metrics', views.view_health_metrics, name='view_health_metrics'),
    path('add_ambulance_details', views.add_ambulance_details, name='add_ambulance_details'),
    path('view_ambulance_details', views.view_ambulance_details, name='view_ambulance_details'),
    path('counseling/report/', views.counseling_report, name='counseling_report'),
    path('counseling/report/', views.generate_pdf_counselling, name='generate_pdf_counselling'),
    # path('counseling/report/pdf/', views.CounselingReportPDF.as_view(), name='counseling_report_pdf'),
    path('meeting', views.videocall_counselor, name='meeting'),
    path('join_room', views.join_room, name='join_room'),
    path('home_counselor', views.home_counselor, name='home_counselor'),


    # PASSWORD RESET
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('confirm-appointment/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),
    path('complete-appointment/<int:appointment_id>/', views.complete_appointment, name='complete_appointment'),
    path('appointment_details', views.appointment_details, name='appointment_details'),


# flutter
    path('api/healthcare-tips/', views.healthcare_tips_view, name='healthcare_tips'),
    path('api/ambulances/', views.ambulance_list_view, name='ambulance_list'),

    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)