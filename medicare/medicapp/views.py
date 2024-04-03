import requests
from .models import Profile
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime, timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from medicapp.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from medicapp.models import Treatment
from django.contrib.auth import login as auth_login
import qrcode
import base64
from math import radians,sin,cos,sqrt,atan2

#REGISTRATOIN
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('sname')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        Cpassword = request.POST.get('cpwd')

        if password == Cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')
            else:
                user = User.objects.create_user(first_name= first_name,last_name=last_name,username=username, email=email,password=password)
                user.save()
                messages.info(request, "Account Created Successfully")
                return redirect('login') 
        else:
            messages.info(request, "Passwords do not match")
            return redirect('register')
    return render(request, 'register.html')


#LOGIN
def login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)


        try:
            user_role = UserRole.objects.get(user=user)
            user_role_name = user_role.role
        except UserRole.DoesNotExist:
            user_role_name = None

        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif user_role_name == 'Doctor':
                 return redirect ('doctor')
            else:
                return redirect('patient')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

#FORGOT PASSWORD
def forgot(request):
    return render(request, 'forgot.html')

@login_required()


#LOGOUT
def user_logout(request):
    logout(request)
    return redirect('index')

def patient_home(request):
	appointment = Treatment.objects.filter(approved=True).count()
	medical1 = Medical.objects.filter(medicine='See Doctor').count()
	medical2 = Medical.objects.all().count()
	medical3 = int(medical2) - int(medical1)
	user_id = request.user.id
	user_profile = Profile.objects.filter(user_id=user_id)  
	return render(request, 'patient/home.html')

#INDEX PAGE
def index(request):
    return render(request, 'index.html')

#CREATE PROFILE
def create_profile(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        username = request.user.username
        full_name = request.POST.get('full_name')
        birth_date_str = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')  

        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            birth_date = None 

        if profile:
            profile.birth_date = birth_date
            profile.gender = gender
            profile.full_name = full_name
            profile.phone_number = phone_number  
            profile.save()
        else:
            profile = Profile.objects.create(
                user=request.user,
                birth_date=birth_date,
                gender=gender,
                full_name=full_name,
                phone_number=phone_number  
            )

        messages.success(request, 'Profile Updated')
        return redirect('diagnosis')

    if profile:
        return redirect('diagnosis')
    else:
        choice = ['1', '0']
        gender = ["Male", "Female"]
        context = {"profile": profile, "choice": choice, "gender": gender}
        return render(request, 'patient/create_profile.html', context)


 
#DIAGNOSIS FORM
def diagnosis(request):
	symptoms = ['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain','stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation','redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails','swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)','depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling','silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
	symptoms = sorted(symptoms)
	context = {'symptoms':symptoms, 'status':'1'}
	return render(request, 'patient/diagnosis.html', context)

#DISEASE PREDICTION
import joblib
import numpy as np
from django.http import JsonResponse
from .models import Medical  

nb_model = joblib.load('model/naive_bayes.pkl')

list_a = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremities', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

@csrf_exempt
def MakePrediction(request):
    s1 = request.POST.get('s1')
    s2 = request.POST.get('s2')
    s3 = request.POST.get('s3')
    s4 = request.POST.get('s4')
    s5 = request.POST.get('s5')
    id = request.POST.get('id')

    list_b = [s1, s2, s3, s4, s5]
    list_c = [0] * len(list_a)
    for symptom in list_b:
        if symptom in list_a:
            list_c[list_a.index(symptom)] = 1
    test = np.array(list_c).reshape(1, -1)
    prediction = nb_model.predict(test)
    result = prediction[0]
    a = Medical(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, disease=result, patient_id=id)
    a.save()

    return JsonResponse({'status': result})

#DISPLAY RESULT
def patient_result(request):
    userid = request.user.id
    disease = Medical.objects.all().filter(patient_id=userid)
    context = {'disease':disease,'status':'1'}
    return render(request,'patient/result.html',context)

#MAKE APPOINTMENT
@csrf_exempt
def MakeAppointment(request):
	disease = request.POST.get('disease')
	userid = request.POST.get('userid')

	try:
		check_medical = Treatment.objects.filter(medical_id=disease).exists()
		if(check_medical == False):
			a = Treatment(medical_id=disease, patient_id=userid)
			a.save()
			return JsonResponse({'status':'saved'})
		else:
			print('Appointment Exist')
			return JsonResponse({'status':'exist'})
	except Exception as e:
		return JsonResponse({'status':'error'})			

#PATIENT APPOINTMENT
def patient_appointment(request):
     user_id = request.user.id
     appointment = Treatment.objects.all().filter(patient_id=user_id)
     context = {'ment':appointment , 'status':1}
     return render(request,'patient/ment.html',context)


#DOCTOR DASHBOARD
def doctor_home(request):
	appointment = Treatment.objects.filter(approved=True).count()
	medical1 = Medical.objects.filter(medicine='See Doctor').count()
	medical2 = Medical.objects.all().count()
	medical3 = int(medical2) - int(medical1)
	
	context = {'ment':appointment, 'drug':medical3}
	return render(request, 'doctor/home.html', context)

#RECOMMEND
def doctor_recommend(request):
    userid = request.user.id
    disease = Medical.objects.all()
    context = {'disease':disease}
    return render(request,'doctor/result.html',context)

#DRUG RECOMMENDATON NAIVE BAYES
@login_required
@csrf_exempt
def MakeMend(request):
    disease = request.POST.get('disease')
    userid = request.POST.get('userid')

    print('Disease ID', disease)
    print('User ID is', userid)

    patient = Profile.objects.get(user_id=Medical.objects.get(pk=disease).patient_id)
    dob = patient.birth_date.year
    age = 2023 - dob
    gender = 1 if patient.gender == 'Male' else 0

    print('Patient Age is', age)
    print('Patient Gender is', gender)

    sick = Medical.objects.get(pk=disease).disease
    print('Patient Disease Diagnosed is', sick)

    disease_list = ['Acne', 'Allergy', 'Diabetes', 'Fungal infection', 'Urinary tract infection', 'Malaria',
                    'Malaria', 'Migraine', 'Hepatitis B', 'AIDS']

    disease_dict = {'Acne': 0, 'Allergy': 1, 'Diabetes': 2, 'Fungal infection': 3, 'Urinary tract infection': 4,
                    'Malaria': 5, 'Malaria': 6, 'Migraine': 7, 'Hepatitis B': 8, 'AIDS': 9}

    if sick in disease_list:
        print('AI Got Drug For This Disease')
        print(disease_dict.get(sick))
        new_sick = disease_dict.get(sick)

        test = [new_sick, gender, age]
        print(test)
        test = np.array(test).reshape(1, -1)

        clf = joblib.load('model/medical_nb.pkl')
        prediction = clf.predict(test)
        predicted_disease = prediction[0]
        print('Predicted Disease Is', predicted_disease)

        try:
            check_medical = Medical.objects.filter(patient_id=disease).exists()
            if not check_medical:
                Medical.objects.filter(pk=disease).update(medicine=predicted_disease)
                return JsonResponse({'status': 'recommended'})
            else:
                print('Drug Exist')
            return JsonResponse({'status': 'exist'})
        except Exception as e:
            print(e)
    else:
        print('AI Can Not Recommend Drug')
        Medical.objects.filter(pk=disease).update(medicine='See Doctor')
        return JsonResponse({'status': 'not in store'})
    
#DOCTOR APPOINTMENT
# @login_required
# def doctor_ment(request):
#     user_id = request.user.id
#     appointment = Treatment.objects.all()
#     context = {'ment':appointment, 'status':'1'}
#     return render(request, 'doctor/ment.html', context)

#ADMIN DASHBOARD
def admin_dashboard(request):
    return render(request, 'admin/home.html')


#PATIENT INFO
from django.views.generic import ListView
from .models import Medical, Profile

class PatientListView(ListView):
    model = Medical
    template_name = 'admin/patientinfo1.html'
    context_object_name = 'patients'

    def get_queryset(self):
        queryset = Medical.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_profiles = Profile.objects.filter(user__in=context['patients'].values('patient__id'))
        context['patient_profiles'] = patient_profiles
        return context
    
#ADD DOCTOR
import csv
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor
from django.contrib.auth.models import User
from .models import Doctor, UserRole
from django.shortcuts import redirect, render, get_object_or_404

def add_doctor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        license_no = request.POST['license_no']
        email = request.POST['email']
        phone = request.POST['phone']
        specialization = request.POST['specialization']  # Add this line to get specialization


        # Check if a user with the same email already exists
        existing_user = User.objects.filter(username=email).first()

        if existing_user:
            messages.error(request, 'User with this email already exists')
        else:
            csv_file_path = 'doctor_dataset/docinfo.csv'
            match_found = False

            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    if (
                        row['First Name'] == first_name and
                        row['Last Name'] == last_name and
                        row['License Number'] == license_no
                    ):
                        match_found = True
                        break

            if match_found:
                # Create a new user
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )

                # Set the default password for the user
                user.set_password("Doctor@medicare7")
                user.save()

                # Create a new Doctor
                doctor = Doctor(
                    user=user,
                    specialization = specialization,
                    license_no=license_no,
                    phone=phone,
                )
                doctor.save()

                # Set the user's role to 'Doctor'
                user_role = UserRole(user=user, role='Doctor')
                user_role.save()

                subject = 'Your account has been created'
                message = 'Your account has been created.Use password Doctor@medicare7 to login'
                from_email = settings.EMAIL_HOST_USER  # Your sender email address
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Doctor added successfully')
            else:
                messages.error(request, 'No matching records found')

        

    return render(request, 'admin/add_doctor.html', context={'messages': messages.get_messages(request)})



#VIEW DOCTORS
def doctor_info(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/doctorinfo.html', {'doctors': doctors})

#EDIT DOCTOR DETAILS 
# def edit_doctor(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)

#     if request.method == 'POST':
#         doctor.first_name = request.POST['first_name']
#         doctor.last_name = request.POST['last_name']
#         doctor.email = request.POST['email']
#         doctor.license_no = request.POST['license_no']
#         doctor.phone = request.POST['phone']
#         doctor.save()
#         return redirect('doctor_info')

#     return render(request, 'admin/edit_doctor.html', {'doctor': doctor})

# # DELETE DOCTOR
# def delete_doctor(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)

#     if request.method == 'POST':
#         # Delete the associated user
#         user = doctor.user
#         user.delete()

#         # Delete the doctor record
#         doctor.delete()

#         # Delete the user role record (if exists)
#         try:
#             user_role = UserRole.objects.get(user=user)
#             user_role.delete()
#         except UserRole.DoesNotExist:
#             pass

#         return redirect('doctor_info')

#     return render(request, 'admin/delete_doctor.html', {'doctor': doctor})

#EXPORT PDF OF PATIENTINFO
import tablib
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import Medical

def export_pdf(request):
    patients = Medical.objects.all()
    data = [["Name", "Symptom 1", "Symptom 2", "Symptom 3", "Symptom 4", "Symptom 5", "Disease Diagnosed", "Treatment Recommended"]]
    for patient in patients:
        data.append([
            patient.patient.profile.full_name,
            patient.s1,
            patient.s2,
            patient.s3,
            patient.s4,
            patient.s5,
            patient.disease,
            patient.medicine
        ])

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Define column widths for the table
    col_widths = [100, 60, 60, 60, 60, 60, 100, 100]  # Adjust widths as needed

    # Define table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Reduced font size to 10 for data rows
        ('SIZE', (0, 0), (-1, 0), 8),
    ])

    # Create the table with specified column widths and apply the style
    table = Table(data, colWidths=col_widths)
    table.setStyle(style)

    # Add a title to the PDF
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading_style.alignment = 1  # 0=Left, 1=Center, 2=Right
    heading = Paragraph("Medicare - Patient Records", heading_style)


    # Wrap the table in KeepTogether to ensure it doesn't break across pages
    elements.append(KeepTogether([heading, table]))

    # Build the PDF and prepare the response
    doc.build(elements)
    buffer.seek(0)
    response = FileResponse(buffer, as_attachment=True, filename='patient_information.pdf')
    return response

#EXPORT CSV OF PATIENTINFO
import csv
from django.http import HttpResponse
from .models import Medical

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_dataset.csv"'

    writer = csv.writer(response)
    writer.writerow(['Symptom 1', 'Symptom 2', 'Symptom 3', 'Symptom 4', 'Symptom 5', 'Disease Diagnosed', 'Treatment Recommended'])

    patients = Medical.objects.all()

    for patient in patients:
        writer.writerow([patient.s1, patient.s2, patient.s3, patient.s4, patient.s5, patient.disease, patient.medicine])
    return response


#ADMIN DASHBOARD OVERVIEW
from django.shortcuts import render
from medicapp.models import Medical, Treatment, User  

def home(request):
    drug_count = Medical.objects.count()
    patient_count = User.objects.filter(groups__name='Patients').count()
    appointment_count = Treatment.objects.count()
    doctor_count = User.objects.filter(groups__name='Doctors').count()

    context = {
        'drug': drug_count,
        'patient': patient_count,
        'ment': appointment_count,
        'doctor': doctor_count,
    }

    return render(request, 'admin/home.html', context)

#VIEW USER PROFILE
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Profile

def user_profile(request):
    user = request.user  
    profile = Profile.objects.get(user=user)  
    return render(request, 'patient/user_profile.html', {'user': user, 'profile': profile})


#VIEW PATIENT INFO
from django.shortcuts import render 
from .models import Medical

def view_patient_info(request):
    patients = Medical.objects.all()
    return render(request, 'doctor/view_patient_info.html', {'patients': patients})


#BOOK APPOINTMENTS
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Doctor



def create_appointment(request):
    return render(request, 'patient/appointments.html')

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id,is_active=True)
    
    if request.method == 'POST':
        # Get the data from the POST request
        date = request.POST.get('date')
        time = request.POST.get('time')
        patient = request.user  # Assuming the patient is the currently logged-in user
        specialization = request.POST.get('id_specialization')
        selected_doctor_id = request.POST.get('id_doctor')
        selected_doctor = get_object_or_404(Doctor, pk=selected_doctor_id,is_active=True)
        
        # Create and save the appointment
        appointment = Appointment(
            date=date,
            time=time,
            patient=patient,
            specialization=specialization,
            doctor=selected_doctor
        )
        appointment.save()
        
        success_message = "Appointment created successfully!"
        return JsonResponse({'success_message': success_message})
    
    else:
        # Render the initial HTML form
        return render(request, 'patient/appointments.html', {'doctor': doctor})



#PATIENT HOME
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor

@login_required
def patient_home(request):
    doctor = Doctor.objects.first()

    context = {
        'doctor': doctor,
    }

    return render(request, 'patient/home.html', context)


#ACTIVATE DOCTOR
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

@login_required
def activate_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        user = doctor.user
        if user:
            user.is_active = True
            user.save()
            doctor.is_active = True
            doctor.save()
            messages.success(request, f'Doctor {doctor.get_full_name()} has been activated.')
        else:
            messages.error(request, 'Associated user not found.')
        subject = 'Your account has been activated'
        message = 'Your account has been activated successfully.'
        from_email = settings.EMAIL_HOST_USER  
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')

    return redirect(reverse('doctor_info'))  


#DEACTIVATE DOCTOR
@login_required
def deactivate_doctor(request, doctor_id):
    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        user = doctor.user
        if user:
            user.is_active = False
            user.save()
            doctor.is_active = False
            doctor.save()
            messages.success(request, f'Doctor {doctor.get_full_name()} has been deactivated.')
        else:
            messages.error(request, 'Associated user not found.')

        subject = 'Your account has been deactivated'
        message = 'Your account has been deactivated.'
        from_email = settings.EMAIL_HOST_USER 
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found.')

    return redirect(reverse('doctor_info')) 


#VIEW APPOINTMENTS @DOCTOR SIDE
from django.shortcuts import render
from .models import Appointment
from django.contrib.auth.decorators import login_required

@login_required
def doctor_appointments(request):
    doctor = request.user.doctor_profile
    appointments = Appointment.objects.filter(doctor=doctor)

    context = {
        'appointments': appointments
    }

    return render(request, 'doctor/appointments.html', context)


#CONFIRM APPOITMENTS
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Doctor
from django.conf import settings  # Import the settings module

@login_required
def confirm_appointment_doctor(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    if appointment.doctor == request.user.doctor_profile:
        if appointment.status == 'scheduled':
            appointment.status = 'confirmed'
            appointment.save()

            subject = 'Appointment Confirmed'
            message = 'Your appointment is confirmed.'
            from_email = settings.EMAIL_HOST_USER  
            recipient_list = [appointment.patient.email] 
            send_mail(subject, message, from_email, recipient_list)

    return redirect('doctor_appointments')



#APPOITMENT COMPLETED
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment, Doctor
from django.conf import settings 

@login_required
def complete_appointment_doctor(request, appointment_id):
    appointment = Appointment.objects.get(pk=appointment_id)
    if appointment.doctor == request.user.doctor_profile:
        if appointment.status == 'confirmed':
            appointment.status = 'completed'
            appointment.save()
            subject = 'Appointment Completed'
            message = 'Your appointment has been completed.'
            from_email = settings.EMAIL_HOST_USER 
            recipient_list = [appointment.patient.email] 
            send_mail(subject, message, from_email, recipient_list)

    return redirect('doctor_appointments')


#VIEW APPOITMENTS STATUS @PATIENT SIDE
from django.shortcuts import render
from .models import Appointment

def view_appointments(request):
    user_appointments = Appointment.objects.filter(patient=request.user)
    context = {'ment': user_appointments,'status':'1'}
    return render(request, 'patient/view_appointment.html', context)

# def patient_result(request):
#     userid = request.user.id
#     disease = Medical.objects.all().filter(patient_id=userid)
#     context = {'disease':disease,'status':'1'}
#     return render(request,'patient/result.html',context)


#LIST APPOINTMENTS @ADMIN SIDE
from django.shortcuts import render
from .models import Appointment

def list_appointments(request):
    selected_status = request.GET.get('status', 'all')
    if selected_status == 'all':
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(status=selected_status)

    context = {
        'appointments': appointments,
        'selected_status': selected_status,
    }

    return render(request, 'admin/view_appointments.html', context)








from django.http import JsonResponse

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Doctor.objects.filter(specialization=category_id)
    
    # Create a list of dictionaries containing doctor information
    subcategory_options = [{'id': doctor.id, 'name': doctor.get_full_name()} for doctor in subcategories]
    
    return JsonResponse({'subcategories': subcategory_options})



from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



from django.shortcuts import render
from django.conf import settings
from razorpay import Client as RazorpayClient
from .models import Appointment, Payment


def appointment_success(request):
    # Retrieve the appointment instance

    currency = 'INR'
    amount = int(200*100)  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # order id of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    # Create a Payment for the appointment
    payment = Payment.objects.create(
        user=request.user,
        payment_amount=amount,  # Specify the payment amount
        payment_status='Pending',  # Set payment status to "Pending"
    )

    # Render the success template with the necessary context
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'patient/appointment_success.html', context=context)


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            # Get the payment details from the POST request
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            amount=request.POST.get('razorpay_amount', '')

            # Verify the payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,

            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            if result is not None:
                amount = int(200*100)  # Rs. 200

                # Capture the payment
                razorpay_client.payment.capture(payment_id, amount)

                # Save payment details to the Payment model
                # Assuming you have a Payment model defined
                payment = Payment.objects.create(
                    user=request.user,  # Assuming you have a logged-in user
                    payment_amount=amount,
                    payment_status='Success',  # Assuming payment is successful
                )

                # Redirect to a success page with payment details
                return redirect('payment_success')  # Replace 'orders' with your actual success page name or URL
            else:
                # Signature verification failed
                return HttpResponse("Payment signature verification failed", status=400)
        except Exception as e:
            # Handle exceptions gracefully
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
    else:
        # Handle non-POST requests
        return HttpResponse("Invalid request method", status=405)

from .models import Payment

def confirm_payment(request, appointment_id):
    # Retrieve the appointment instance
    appointment = Appointment.objects.get(pk=appointment_id)
    payment = Payment.objects.create(payment_status='Pending')

    # Create a payment for the appointment
    payment = Payment.objects.create(
        user=request.user,
        payment_amount=200.00,  # Specify the payment amount
        payment_status='Pending',  # Set payment status to "Pending"
    )

    # Your payment confirmation logic here

    return render(request, 'payment_success.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Medical
from django.utils import timezone

@login_required
def medical_report(request):
    # Get the currently logged-in user
    current_user = request.user

    # Retrieve the most recent medical record for the user
    try:
        medical_record = Medical.objects.filter(patient=current_user).latest('id')
        
    except Medical.DoesNotExist:
        medical_record = None

    context = {
        'current_user': current_user,
        'medical_record': medical_record,
        'current_datetime': timezone.now(),
        'status':'1'
    }

    return render(request, 'patient/report.html', context)



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.utils import timezone

def generate_pdf(request, medical_record_id):
    # Get the medical record data
    medical_record = Medical.objects.get(id=medical_record_id)
    
    # Prepare the template context
    context = {
        'medical_record': medical_record,
        'current_user': request.user,
    }
    
    # Render the HTML template for the PDF
    template = get_template('patient/medical_report_pdf.html')
    html = template.render(context)
    
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="medical_report.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



# views.py


import random
from .models import Doctor

def your_view(request):
    # Get all active doctors
    active_doctors = Doctor.objects.filter(is_active=True)

    # Check if there are active doctors
    if active_doctors:
        # Select a random doctor from the list
        random_doctor = random.choice(active_doctors)

        # Pass the random_doctor to your template context
        context = {'random_doctor': random_doctor}

        return render(request, 'your_template.html', context)
    else:
        # Handle the case when there are no active doctors
        return render(request, 'no_active_doctors_template.html')


def payment_success(request):
    context = {'status':'1'}
    return render (request,'patient/payment_success.html',context)



# from django.http import JsonResponse

# def chart_data(request):
#     # Retrieve data from your models, process it, and prepare it for the charts
#     data = {
#         "drug": 10,
#         "patient": 50,
#         "appointment": 30,
#         "doctor": 5,
#         "male_patient_count": 35,
#         "female_patient_count": 15,
#     }
#     return JsonResponse(data)



#CHARTS
from django.http import JsonResponse
from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .models import Appointment

def monthly_appointment_counts(request):
    # Filter appointments with 'confirmed' and 'completed' statuses
    appointments = Appointment.objects.filter(status__in=['confirmed', 'completed'])

    # Group appointments by month and count them
    monthly_counts = appointments.annotate(
        month=ExtractMonth('date')
    ).values(
        'month'
    ).annotate(
        total_appointments=Count('id')
    ).order_by(
        'month'
    )

    # Convert the result to a list of dictionaries
    result = [{'month': entry['month'], 'total_appointments': entry['total_appointments']} for entry in monthly_counts]

    return JsonResponse({'monthly_counts': result})


# views.py
from django.http import JsonResponse
from django.db.models import Count  # Import Count
from matplotlib.figure import Figure
from io import BytesIO
import base64
import matplotlib.pyplot as plt
from .models import Medical

def disease_distribution_chart(request):
    # Retrieve data for disease distribution
    diseases = Medical.objects.values('disease').annotate(count=Count('id'))  # Use Count

    labels = [disease['disease'] for disease in diseases]
    counts = [disease['count'] for disease in diseases]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.

    # Convert the chart to an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.read()).decode()

    # Prepare JSON response
    data = {
        'chart_image': chart_image,
        'labels': labels,
        'counts': counts,
    }

    return JsonResponse(data)


# import json
# import matplotlib.pyplot as plt
# from io import BytesIO
# import base64
# from django.http import JsonResponse
# from .models import Payment  # Import your Payment model

# def payment_status_pie_chart(request):
#     # Retrieve data for payment status distribution
#     payment_statuses = Payment.objects.values('payment_status').annotate(count=Count('id'))

#     labels = [status['payment_status'] for status in payment_statuses]
#     counts = [status['count'] for status in payment_statuses]

#     # Create a pie chart
#     fig, ax = plt.subplots()
#     ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
#     ax.axis('equal')

#     # Convert the chart to an image
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     chart_image = base64.b64encode(buffer.read()).decode()

#     # Prepare JSON response
#     data = {
#         'chart_image': chart_image,
#         'labels': labels,
#         'counts': counts,
#     }

#     return JsonResponse(data)

# medicapp/views.py
from django.shortcuts import render, redirect
from medicapp.models import PrescriptionRefill

from django.shortcuts import render, get_object_or_404, redirect
from .models import Treatment, PrescriptionRefill

@login_required
def refill_request_view(request, username):
    # Ensure that the provided username matches the currently logged-in user
    user_treatments = Treatment.objects.filter(patient=request.user)

    return render(request, 'patient/refill_request_form.html', {'user_treatments': user_treatments})


# Assuming you have a model called Counselor in your models.py
# from django.shortcuts import render, redirect
# from django.views import View
# from django.contrib import messages
# from .models import Counselor

# class AddCounselorView(View):
#     template_name = 'admin/add_counselor.html'  # Path to your HTML template

#     def get(self, request):
#         return render(request, self.template_name)

#     def post(self, request):
#         # Retrieve data from the submitted form
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         email = request.POST.get('email')

#         # Validate the data (you can use Django forms for more complex validation)
#         if not (first_name and last_name and email):
#             messages.error(request, 'All fields are required.')
#             return redirect('add_counselor')  # Redirect to the same page in case of errors

#         # Save the counselor to the database
#         counselor = Counselor.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             # Add other fields as needed
#         )

#         messages.success(request, 'Counselor added successfully.')
#         return redirect('add_counselor')  # Redirect to the same page after successful submission


from django.contrib.auth.models import User
from django.contrib import messages
from .models import Counselor

def add_counselor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        existing_user = User.objects.filter(username=email).first()

        if existing_user:
            messages.error(request, 'User with this email already exists')
        else:
            # Create a new user
            user = User.objects.create_user(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )

            # Create a new Counselor
            counselor = Counselor(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            counselor.save()

            # Set the default password for the user
            default_password = "Counselor@Medicare"
            user.set_password(default_password)
            user.save()

            messages.success(request, 'Counselor added successfully. Login credentials sent to the email.')

            # You might want to send an email to the counselor here

    return render(request, 'admin/add_counselor.html', context={'messages': messages.get_messages(request)})



# views.py
from django.shortcuts import render
from .models import Counselor

def counselor_list(request):
    counselors = Counselor.objects.all()
    return render(request, 'admin/counselorinfo.html', {'counselors': counselors})

def login_counselor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the email exists in the Counselor model
        try:
            counselor = Counselor.objects.get(email=email)
        except Counselor.DoesNotExist:
            counselor = None

        if counselor is not None and counselor.user.check_password(password):
            # Login the user and redirect to a success page
            auth_login(request, counselor.user)
            return redirect('base_counselor')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'counselor/login_counselor.html')

def base_counselor(request):
    return render(request, 'counselor/base_counselor.html')

def home_counselor(request):
    return render(request, 'counselor/home_counselor.html')

def patient_counselling(request):
    return render(request, 'patient/patient_counselling.html')

# views.py

from django.shortcuts import render, redirect
from .models import Hospital

def add_hospital(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        opening_time = request.POST.get('opening_time')
        closing_time = request.POST.get('closing_time')
        opening_days = request.POST.get('opening_days')
        hospital_image = request.FILES.get('hospital_image')
        avgrating = request.POST.get('avgrating')

        # Create a new Hospital object and save it to the database
        hospital = Hospital.objects.create(
            name=name,
            email=email,
            city=city,
            state=state,
            country=country,
            contact=contact,
            address=address,
            latitude=latitude,
            longitude=longitude,
            opening_time=opening_time,
            closing_time=closing_time,
            opening_days=opening_days,
            hospital_image=hospital_image,
            avgrating=avgrating
        )
        
        # Redirect to a success page or any other desired URL
        return redirect('home')  # Change 'home' to the appropriate URL

    return render(request, 'admin/add_hospital.html')

# def login_counselor(request):
#     # Your logic for counselor login goes here
#     return render(request, 'counselor/login_counselor.html')



from math import radians,sin,cos,sqrt,atan2
from .models import UserSellerDistance

def nearby_hospital(request):
    user_profile = Profile.objects.get(user=request.user)
    sellers = Hospital.objects.all()
    nearby_sellers = []

    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        if latitude is not None and longitude is not None:
            user_profile.latitude = float(latitude)  # Convert to float
            user_profile.longitude = float(longitude)  # Convert to float
            user_profile.save()

    latitude = user_profile.latitude
    longitude = user_profile.longitude
    
    for seller in sellers:
        if latitude is not None and longitude is not None:
            # Calculate distance for each seller using haversine
            distance = haversine(float(seller.latitude), float(seller.longitude), user_profile.latitude, user_profile.longitude)  # Convert seller coordinates to float
            
            UserSellerDistance.objects.update_or_create(
                user=request.user,
                hospital=seller,
                defaults={'distance': distance}
            )
        
    userseller = UserSellerDistance.objects.filter(user=request.user)
    nearby_sellers = userseller.filter(
        distance__isnull=False,
        user=request.user,
    ).order_by('distance')

    context = {
        'nearby_sellers': nearby_sellers,
    }

    return render(request, 'patient/nearbyhospital.html', context)


def haversine(lat1, lon1, lat2, lon2):
    # Helper function to convert coordinate to float, treating None as 0.0
    def convert_coord(coord):
        return float(coord) if coord is not None else 0.0
      
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(convert_coord, [lat1, lon1, lat2, lon2])  # Fixed here
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371.0 * c  # Radius of Earth in kilometers

    return distance

def view_hospital(request):
    seller=Hospital.objects.all
    return render(request, 'admin/view_hospital.html',{'seller':seller})

def counselor_appointment(request):
    if request.method == 'POST':
        counselor_id = request.POST.get('counselor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        # Create a new AppointmentCounselling object
        appointment = AppointmentCounselling(
            patient=request.user,  # Assuming user is logged in
            counselor_id=counselor_id,
            date=appointment_date,
            time=appointment_time,
            reason=reason
        )
        appointment.save()
        return redirect('patient_counselling')  # Redirect to a success page
    else:
        counselors = Counselor.objects.all()
        return render(request, 'patient/counselling_appointment.html', {'counselors': counselors})

from django.shortcuts import render, redirect
from .models import Counselor, AppointmentCounselling
from django.contrib.auth.decorators import login_required


    



from django.shortcuts import render
from .models import AppointmentCounselling

def counselor_appointments(request):
    # Retrieve appointments for the logged-in counselor
    counselor = request.user.counselor
    appointments = AppointmentCounselling.objects.filter(counselor=counselor)
    return render(request, 'counselor/appointments_made.html', {'appointments': appointments})

from django.core.mail import send_mail
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(AppointmentCounselling, id=appointment_id)
    user=request.user
    if request.method == 'POST':
        appointment.status = 'confirmed'
        appointment.save()
        subject = 'Your appointment has been confirmed'
        message = 'Your appointment has been confirmed'
        from_email = settings.EMAIL_HOST_USER  # Your sender email address
        recipient_list = [user.email]
        print(recipient_list)
        send_mail(subject, message, from_email, recipient_list)
        # You can add additional logic here, such as sending notifications
        return redirect('counselor_appointments')  # Redirect back to appointments page
    return render(request, 'counselor/appointments_made.html', {'appointment': appointment})

def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(AppointmentCounselling, id=appointment_id)
    user=request.user
    if request.method == 'POST':
        appointment.status = 'completed'
        appointment.save()
        subject = 'Your appointment has been completed'
        message = 'Your appointment has been completed'
        from_email = settings.EMAIL_HOST_USER  # Your sender email address
        recipient_list = [user.email]
        print(recipient_list)
        send_mail(subject, message, from_email, recipient_list)
        # You can add additional logic here, such as updating records
        return redirect('counselor_appointments')  # Redirect back to appointments page
    return render(request, 'counselor/appointments_made.html', {'appointment': appointment})



# def appointment_details(request):
#     # Assuming you have a way to identify the current user, 
#     # such as through authentication or session data
#     current_user = request.user
    
#     # Query the database for the current user's appointment
#     appointment = Appointment.objects.filter(patient=current_user).first()
    
#     # Assuming 'status' is a field in the Appointment model
#     status = appointment.get_status_display() if appointment else "No appointment found"
    
#     context = {
#         'appointment': appointment,
#         'status': status
#     }
#     return render(request, 'patient/appointment_details.html', context)

@login_required
def qrscan(request, appointment_id):
    # Retrieve the parameters from the query string or POST data
    user = request.user

    # Check if the current user is a seller
        # If the user is a seller, retrieve the seller profile
    current_counselor = Counselor.objects.get(user=user)

        # Retrieve the orders for the current seller
    seller_orders = AppointmentCounselling.objects.filter( counselor=current_counselor, id=appointment_id)
    seller_orders_item = AppointmentCounselling.objects.get( counselor=current_counselor, id=appointment_id)


    if seller_orders_item.status == 'confirmed':
            # Check if there are matching OrderItem objects
        if seller_orders.exists():

            seller_orders_item.status = 'Completed'
            seller_orders_item.save()
            qr_error_message = "guyvgyv"

            context = {
                        'appointments': seller_orders,
                            # 'qr_error_message': qr_error_message,
                        }
            return render(request, 'counselor/appointments_made.html', context)
            
        else:
            appointments = AppointmentCounselling.objects.filter(counselor=current_counselor)
            qr_error_message = "This appointment does not belong to your list of appointments."
            context = {
                    'qr_error_message': qr_error_message,
                    'appointments': appointments,
            }
            return render(request, 'counselor/appointments_made.html', context)
    else:

        appointments = AppointmentCounselling.objects.filter(counselor=current_counselor)
        qr_error_message = "This appointment is not confirmed"
        context = {
                    'qr_error_message': qr_error_message,
                    'appointments': appointments,
            }
        return render(request, 'counselor/appointments_made.html', context)
    # Redirect to the sellerorder page with an error message

from .models import Review
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity
    return sentiment_score

def map_sentiment_to_rating(sentiment_score):
    if sentiment_score >= 0.5:
        return 5
    elif sentiment_score >= 0.2:
        return 4
    elif sentiment_score >= -0.2:
        return 3
    elif sentiment_score >= -0.5:
        return 2
    else:
        return 1

@login_required
def submit_review(request):
  
    if request.method == 'POST':
        print(request.POST)
        print(123123)
        counselor_id = request.POST.get('seller_id')
        counselor = Counselor.objects.get(id=counselor_id)
        description = request.POST.get('description')
        review_id = request.POST.get('review_id')  # Get the review_id from the form

        # Sentiment Analysis using TextBlob
        sentiment_score = analyze_sentiment(description)

        # Calculate the rating based on sentiment score
        star_rating = map_sentiment_to_rating(sentiment_score)

        if review_id:
            # If review_id is available, it's an edit action
            review = Review.objects.get(review_id=review_id)
            review.description = description
            review.rating = star_rating  # Update the rating based on sentiment
            review.save()
        else:
            # It's an add action
            review = Review.objects.create(
                user=request.user,
                rating=star_rating,  # Use calculated rating
                description=description,
                counselor=counselor,
                review_status='REVIEWED',
            )
        print(review_id)
       
        # Redirect to a success page or the product detail page
        return redirect('appointment_details')
    
def appointment_details(request):
    # Retrieve the current user's appointments
    user = request.user
    appointments = AppointmentCounselling.objects.filter(patient=user)
    
    appointment_items = []
    for appointment in appointments:
        review = Review.objects.filter(user=request.user, counselor=appointment.counselor ).first()

        if review:
            review_status = review.review_status
            review_id = review.pk
            review_desc = review.description
        else:
            review_status = 'Pending'
            review_id = None
            review_desc = None
            

        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
        qr.add_data(f'Appointment ID: {appointment.id}\n')            
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        buffered = BytesIO()
        qr_img.save(buffered, format="PNG")
        appointment.qr_code_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

        appointment_items.append((appointment,review_status,review_id,review_desc))
    return render(request, 'patient/appointment_details.html', {'appointment_items': appointment_items})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg
@login_required
def submit_feedback(request):
   
    return render(request, 'patient/feedback_form.html')


from django.shortcuts import render

def counselor_feedback(request):
    
    counselor = Counselor.objects.get(user=request.user)
    
    allreviews = Review.objects.filter(counselor=counselor)    
    avg_rating = allreviews.aggregate(Avg('rating'))['rating__avg'] or 0
    return render(request, 'counselor/feedback_list.html',{'allreviews':allreviews,
        'avg_rating':avg_rating,'counselor':counselor})



from django.shortcuts import render, redirect
from .models import Counselor

def counselor_list(request):
    counselors = Counselor.objects.all()
    return render(request, 'admin/counselor_info.html', {'counselors': counselors})

def activate_counselor(request, counselor_id):
    counselor = Counselor.objects.get(pk=counselor_id)
    counselor.is_active = True
    counselor.save()
    return redirect('counselor_list')

def deactivate_counselor(request, counselor_id):
    counselor = Counselor.objects.get(pk=counselor_id)
    counselor.is_active = False
    counselor.save()
    return redirect('counselor_list')


from django.shortcuts import render
from .models import AppointmentCounselling

def counselor_appointments_list(request):
    appointments = AppointmentCounselling.objects.all()  # Query to retrieve all appointments
    return render(request, 'admin/counselor_appointments.html', {'appointments': appointments})


# medicapp/views.py

from django.shortcuts import render, redirect
from .models import HealthcareTip
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_healthcare_tip(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        image = request.FILES.get('image') if 'image' in request.FILES else None

        # Create and save the HealthcareTip object
        tip = HealthcareTip(title=title, description=description, category=category, image=image)
        tip.save()

        # Display success message
        messages.success(request, 'Healthcare Tip added successfully!')
        
        # Redirect to a success page or any other appropriate page
        return redirect('home')  # Change 'counselor_list' to the appropriate URL name

    return render(request, 'admin/add_healthcare_tip.html')


# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .models import HealthcareTip


# def like_tip(request, tip_id):
#     tip = get_object_or_404(HealthcareTip, id=tip_id)
#     tip.likes_count += 1
#     tip.save()
#     return JsonResponse({'likes_count': tip.likes_count})

# def share_tip(request, tip_id):
#     tip = get_object_or_404(HealthcareTip, id=tip_id)
#     tip.shares_count += 1
#     tip.save()
#     return JsonResponse({'shares_count': tip.shares_count})

# def bookmark_tip(request, tip_id):
#     tip = get_object_or_404(HealthcareTip, id=tip_id)
#     tip.bookmarks_count += 1
#     tip.save()
#     return JsonResponse({'bookmarks_count': tip.bookmarks_count})


# def view_healthcare_tips(request):
#     healthcare_tips = HealthcareTip.objects.all()
#     return render(request, 'patient/view_healthcare_tips.html', {'healthcare_tips': healthcare_tips})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from .models import HealthcareTip, LikedTip, BookmarkedTip

def view_healthcare_tips(request):
    healthcare_tips = HealthcareTip.objects.all()
    session_key = request.session.session_key
    liked_tips = LikedTip.objects.filter(session_key=session_key).values_list('tip_id', flat=True)
    bookmarked_tips = BookmarkedTip.objects.filter(session_key=session_key).values_list('tip_id', flat=True)
    return render(request, 'patient/view_healthcare_tips.html', {'healthcare_tips': healthcare_tips, 'liked_tips': liked_tips, 'bookmarked_tips': bookmarked_tips})

def like_tip(request, tip_id):
    if request.user.is_authenticated:
        tip = get_object_or_404(HealthcareTip, id=tip_id)
        session_key = request.session.session_key
        try:
            liked_tip = LikedTip.objects.get(tip=tip, session_key=session_key)
            tip.likes_count -= 1
            liked_tip.delete()
        except ObjectDoesNotExist:
            tip.likes_count += 1
            LikedTip.objects.create(tip=tip, session_key=session_key)
        tip.save()
        return JsonResponse({'likes_count': tip.likes_count})
    else:
        return JsonResponse({'error': 'User not authenticated'})

def share_tip(request, tip_id):
    tip = get_object_or_404(HealthcareTip, id=tip_id)
    tip.shares_count += 1
    tip.save()
    return JsonResponse({'shares_count': tip.shares_count})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import HealthcareTip, LikedTip, BookmarkedTip
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

def bookmark_tip(request, tip_id):
    if request.user.is_authenticated:
        tip = get_object_or_404(HealthcareTip, id=tip_id)
        session_key = request.session.session_key
        try:
            bookmarked_tip = BookmarkedTip.objects.get(tip=tip, session_key=session_key)
            bookmarked_tip.delete()
            message = 'Bookmark removed'
        except ObjectDoesNotExist:
            BookmarkedTip.objeclts.create(tip=tip, session_key=session_key)
            message = 'Bookmark added'
        return JsonResponse({'message': message})
    else:
        return JsonResponse({'error': 'User not authenticated'})


def view_healthcare_tips_admin(request):
    healthcare_tips = HealthcareTip.objects.all()
    return render(request, 'admin/view_healthcare_tips.html', {'healthcare_tips': healthcare_tips})



# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthcareTip

def edit_healthcare_tip(request, tip_id):
    tip = get_object_or_404(HealthcareTip, id=tip_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        # Update the healthcare tip object with the new data
        tip.title = title
        tip.description = description
        tip.category = category
        tip.save()
        return redirect('home')  # Redirect back to the list view
    return render(request, 'admin/edit_healthcare_tip.html', {'tip': tip})


from django.shortcuts import render, redirect, get_object_or_404
from .models import HealthcareTip

def delete_healthcare_tip(request, tip_id):
    tip = get_object_or_404(HealthcareTip, id=tip_id)
    if request.method == 'POST':
        tip.delete()
        return redirect('home')  # Redirect back to the list view
    return render(request, 'admin/delete_healthcare_tip.html', {'tip': tip})


from django.contrib.auth.decorators import login_required
from django.utils import timezone

# @login_required
# def counselling_report(request):
#     # Retrieve recent appointments for the current patient
#     recent_appointments = AppointmentCounselling.objects.filter(patient=request.user).order_by('-date', '-time')[:5]
#     return render(request, 'patient/counselling_report.html', {'appointments': recent_appointments})

# @login_required
# def generate_pdf_report(request):
#     # Retrieve all appointments for the current patient
#     appointments = AppointmentCounselling.objects.filter(patient=request.user)

#     # Create a response object
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="counseling_report.pdf"'

#     # Create a PDF document
#     doc = SimpleDocTemplate(response, pagesize=letter)
    
#     # Create a list to hold the data for the table
#     data = [['Date', 'Time', 'Counselor', 'Reason', 'Status']]

#     # Add data for each appointment to the list
#     for appointment in appointments:
#         counselor_name = appointment.counselor.get_full_name()
#         data.append([appointment.date, appointment.time, counselor_name, appointment.reason, appointment.status])

#     # Create a table and style
#     table = Table(data)
#     style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#                         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#                         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#                         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#                         ('GRID', (0, 0), (-1, -1), 1, colors.black)])

#     # Apply the style to the table
#     table.setStyle(style)

#     # Add the table to the PDF document
#     doc.build([table])

#     return response

def health_tracker_home(request):
    return render(request, 'patient/health_tracker_home.html')


# from django.shortcuts import render, redirect
# from .models import HealthMetric
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages

# @login_required
# def health_tracker(request):
#     if request.method == 'POST':
#         metric_type = request.POST.get('metric_type')
#         value = request.POST.get('value')
#         user = request.user

#         # Save the health metric to the database
#         HealthMetric.objects.create(user=user, metric_type=metric_type, value=value)

#         messages.success(request, 'Health metric recorded successfully.')
#         return redirect('health_tracker')

#     return render(request, 'patient/health_tracker.html')


# flutter



from django.http import JsonResponse
from .models import HealthcareTip

def healthcare_tips_view(request):
    healthcare_tips = HealthcareTip.objects.all()
    data = [{'title': tip.title,
             'description': tip.description,
             'category': tip.category,
             'date_added': tip.date_added.strftime("%Y-%m-%d %H:%M:%S"),
             'image': tip.image.url if tip.image else None,
             'likes_count': tip.likes_count,
             'shares_count': tip.shares_count,
             'bookmarks_count': tip.bookmarks_count} for tip in healthcare_tips]
    return JsonResponse(data, safe=False)


from django.shortcuts import render, redirect
from .models import Ambulance

def add_ambulance_details(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        location = request.POST.get('location')
        vehicle_number = request.POST.get('vehicle_number')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_capacity = request.POST.get('vehicle_capacity')
        driver_name = request.POST.get('driver_name')
        
        # Create and save the AmbulanceDetails object
        ambulance = Ambulance(
            contact_number=contact_number,
            location=location,
            vehicle_number=vehicle_number,
            vehicle_model=vehicle_model,
            vehicle_capacity=vehicle_capacity,
            driver_name=driver_name
        )
        ambulance.save()
        
        # Redirect to a success page or any other page as needed
        return redirect('home')  # Replace 'success_page' with the name of your success page URL pattern
        
    return render(request, 'admin/add_ambulance_details.html')



# ambulance flutter
from django.http import JsonResponse
from .models import Ambulance

def ambulance_list_view(request):
    ambulances = Ambulance.objects.all()
    data = [{'contact_number': ambulance.contact_number,
             'location': ambulance.location,
             'vehicle_number': ambulance.vehicle_number,
             'vehicle_model': ambulance.vehicle_model,
             'vehicle_capacity': ambulance.vehicle_capacity,
             'driver_name': ambulance.driver_name} for ambulance in ambulances]
    return JsonResponse(data, safe=False)


def view_ambulance_details(request):
    ambulance = Ambulance.objects.all()
    verbose_name_plural = Ambulance._meta.verbose_name_plural.title()
    return render(request, 'admin/view_ambulance_details.html', {'ambulance': ambulance, 'verbose_name_plural': verbose_name_plural})



from django.shortcuts import render
from .models import AppointmentCounselling

def counseling_report(request):
    # Get the latest counseling appointment for the patient
    latest_counseling = AppointmentCounselling.objects.filter(patient=request.user).latest('date')

    # Get the related patient and counselor information
    patient = latest_counseling.patient
    counselor = latest_counseling.counselor

    context = {
        'patient': patient,
        'counselor': counselor,
        'counseling': latest_counseling,
    }

    return render(request, 'patient/counselling_report.html', context)

#VIDEO CONFERENCE
def videocall_counselor(request):
    return render(request, 'counselor/video_conference.html',{'name': request.user.first_name + " " + request.user.last_name})


# def join_room(request):
#     if request.method =='POST':
#         roomID = request.POST['roomID']
#         return redirect("/videocall_counselor?roomID="+3527)
#     return render(request,'patient/video_conference.html')

def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID="+ roomID)
    return render(request,'patient/join_room.html')

#HEALTH MATRICES
# from django.shortcuts import render, redirect
# from .models import HealthMetric
# from django.contrib import messages

# def record_health_metric(request):
#     if request.method == 'POST':
#         # Retrieve data from the POST request
#         weight = request.POST.get('weight')
#         systolic_bp = request.POST.get('systolic_bp')
#         diastolic_bp = request.POST.get('diastolic_bp')
#         blood_sugar = request.POST.get('blood_sugar')
#         heart_rate = request.POST.get('heart_rate')
#         print(heart_rate)
#         # Create a new HealthMetric object and save it to the database
#         health_metric = HealthMetric.objects.create(
#             user=request.user,
#             weight=float(weight),
#             blood_pressure_systolic=int(systolic_bp),
#             blood_pressure_diastolic=int(diastolic_bp),
#             blood_sugar=float(blood_sugar),
#             heart_rate=int(heart_rate),
#             )
#         messages.success(request, 'Health metric recorded successfully.')
#         return redirect('health_tracker_home')  # Redirect to the home page or another appropriate URL

#     # If the request method is not POST, render the form template
#     return render(request, 'patient/health_tracker.html')



from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter, inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from .models import AppointmentCounselling

def generate_pdf_counselling(request):
    # Fetch counseling session from the database
    counseling_session = AppointmentCounselling.objects.first()  # Assuming you have at least one counseling session

    # Extract patient, counselor, and counseling details
    patient = counseling_session.patient
    counselor = counseling_session.counselor
    counseling_date = counseling_session.date
    counseling_time = counseling_session.time
    counseling_reason = counseling_session.reason
    counseling_status = counseling_session.status

    # Create a buffer for PDF
    buffer = BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Title
    title = "Counseling Report"
    title_style = styles["Title"]
    title_paragraph = Paragraph(title, title_style)

    # Patient Information
    patient_info = [
        ("Name:", patient.profile.full_name),
        ("Gender:", patient.profile.gender),
        ("Phone Number:", patient.profile.phone_number),
    ]
    patient_info_table = Table(patient_info, colWidths=[100, 300])
    patient_info_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    patient_info_table.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)]))

    # Counselor Information
    counselor_info = [
        ("Name:", counselor.get_full_name()),
        ("Email:", counselor.email),
    ]
    counselor_info_table = Table(counselor_info, colWidths=[100, 300])
    counselor_info_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                               ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    counselor_info_table.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)]))

    # Counseling Information
    counseling_info = [
        ("Date:", counseling_date),
        ("Time:", counseling_time),
        ("Reason:", counseling_reason),
        ("Status:", counseling_status),
    ]
    counseling_info_table = Table(counseling_info, colWidths=[100, 300])
    counseling_info_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    counseling_info_table.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)]))

    # Build PDF content
    content = [title_paragraph, Spacer(1, 12), patient_info_table, Spacer(1, 12), counselor_info_table,
               Spacer(1, 12), counseling_info_table]

    # Add content to PDF
    doc.build(content)

    # Get the PDF file content from the buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create an HTTP response with PDF content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="counseling_report.pdf"'
    response.write(pdf_data)
    return response


def home_counselor(request):
    return render(request,'counselor/home_page.html')