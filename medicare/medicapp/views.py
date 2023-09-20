import requests
from .models import Profile
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from medicapp.forms import UserProfileForm
from django.shortcuts import get_object_or_404
from medicapp.models import Treatment


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
@login_required
def doctor_ment(request):
    user_id = request.user.id
    appointment = Treatment.objects.all()
    context = {'ment':appointment, 'status':'1'}
    return render(request, 'doctor/ment.html', context)

#ADMIN DASHBOARD
def admin_dashboard(request):
    return render(request, 'admin/base1.html')


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
from .models import Doctor  

import csv
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor

from django.contrib.auth.models import User
from .models import Doctor, UserRole  # Import the UserRole model

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
                    license_no=license_no,
                    phone=phone,
                )
                doctor.save()

                # Set the user's role to 'Doctor'
                user_role = UserRole(user=user, role='Doctor')
                user_role.save()

                messages.success(request, 'Doctor added successfully')
            else:
                messages.error(request, 'No matching records found')

    return render(request, 'admin/add_doctor.html', context={'messages': messages.get_messages(request)})



#VIEW DOCTORS
def doctor_info(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/doctorinfo.html', {'doctors': doctors})

#EDIT DOCTOR DETAILS 
def edit_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        doctor.first_name = request.POST['first_name']
        doctor.last_name = request.POST['last_name']
        doctor.email = request.POST['email']
        doctor.license_no = request.POST['license_no']
        doctor.phone = request.POST['phone']
        doctor.save()
        return redirect('doctor_info')

    return render(request, 'admin/edit_doctor.html', {'doctor': doctor})

# DELETE DOCTOR
def delete_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        # Delete the associated user
        user = doctor.user
        user.delete()

        # Delete the doctor record
        doctor.delete()

        # Delete the user role record (if exists)
        try:
            user_role = UserRole.objects.get(user=user)
            user_role.delete()
        except UserRole.DoesNotExist:
            pass

        return redirect('doctor_info')

    return render(request, 'admin/delete_doctor.html', {'doctor': doctor})

#EXPORT PDF OF PATIENTINFO
import tablib
from django.http import FileResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
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
    styles = getSampleStyleSheet()
    heading_style = styles['Heading1']
    heading = Paragraph("Patient Information", heading_style)
    elements.append(heading)
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    elements.append(table)
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


from django.shortcuts import render
from .models import Medical

def view_patient_info(request):
    patients = Medical.objects.all()
    return render(request, 'doctor/view_patient_info.html', {'patients': patients})







from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm, CurrentUserForm

@login_required
def book_appointment(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    context = {}

    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        user_form = CurrentUserForm(request.POST)

        if appointment_form.is_valid() and user_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.save()
            return redirect('confirm-appointment')  # Adjust the URL name as needed
    else:
        appointment_form = AppointmentForm()
        user_form = CurrentUserForm(initial={
            'name': request.user.profile.full_name,
            'email': request.user.email,
            'phone': request.user.profile.phone_number,
        })

    context['appointment_form'] = appointment_form
    context['user_form'] = user_form
    context['doctor'] = doctor

    return render(request, 'patient/appointments.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Doctor

@login_required
def patient_home(request):
    # Assuming you are getting the doctor object based on some logic
    doctor = Doctor.objects.first()  # Replace with your logic to get the doctor

    context = {
        'doctor': doctor,
    }

    return render(request, 'patient/home.html', context)






