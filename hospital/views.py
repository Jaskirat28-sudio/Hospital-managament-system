from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Appointment, DoctorAvailability, Hospital
from django.db.models import Q  

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

import datetime


# ---------------- HOME ----------------
def home(request):
    doctors = Doctor.objects.all()
    hospitals = Hospital.objects.all()   

    query = request.GET.get('q')
    if query:
        doctors = doctors.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query)
        )

    context = {
        'doctors': doctors,
        'hospitals': hospitals, 
        'total_doctors': Doctor.objects.count(),
        'total_hospitals': Hospital.objects.count()
    }

    return render(request, 'home.html', context)
# ---------------- REGISTER ----------------
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


# ---------------- LOGIN ----------------
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    availability = DoctorAvailability.objects.filter(doctor=doctor)

    if request.method == "POST":
        patient_name = request.POST['name']
        patient_email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']  
        message = request.POST['message']

        # Convert date → day
        selected_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        selected_day = selected_date.strftime("%a")

        # Convert time
        selected_time = datetime.datetime.strptime(time, "%H:%M").time()

        # Check day availability
        day_availability = availability.filter(day=selected_day).first()

        if not day_availability:
            messages.error(request, "Doctor not available on this day ❌")
            return redirect('book_appointment', doctor_id=doctor.id)

        # Check time range
        if not (day_availability.available_from <= selected_time <= day_availability.available_to):
            messages.error(request, "Selected time is outside availability ⏰")
            return redirect('book_appointment', doctor_id=doctor.id)

        #  CHECK DOUBLE BOOKING 
        existing = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=date,
            appointment_time=time
        ).exists()

        if existing:
            messages.error(request, "This time slot is already booked ❌")
            return redirect('book_appointment', doctor_id=doctor.id)

        #  SAVE
        Appointment.objects.create(
            user=request.user,
            patient_name=patient_name,
            patient_email=patient_email,
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,  
            message=message
        )

        messages.success(request, "Appointment booked successfully ✅")
        return redirect('appointments')

    return render(request, 'book.html', {
        'doctor': doctor,
        'availability': availability
    })


# ---------------- VIEW APPOINTMENTS ----------------
@login_required
def appointments(request):
    data = Appointment.objects.filter(user=request.user)
    return render(request, 'appointments.html', {'appointments': data})


# ---------------- DASHBOARD ----------------
@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user)

    context = {
        'total': appointments.count(),
        'pending': appointments.filter(status="Pending").count(),
        'approved': appointments.filter(status="Approved").count(),
        'rejected': appointments.filter(status="Rejected").count(),
        'appointments': appointments
    }

    return render(request, 'dashboard.html', context)


# ---------------- APPROVE ----------------
@login_required
def approve_appointment(request, id):
    if request.user.is_staff:
        appointment = get_object_or_404(Appointment, id=id)
        appointment.status = "Approved"
        appointment.save()

    return redirect('appointments')


# ---------------- REJECT ----------------
@login_required
def reject_appointment(request, id):
    if request.user.is_staff:
        appointment = get_object_or_404(Appointment, id=id)
        appointment.status = "Rejected"
        appointment.save()

    return redirect('appointments')


# ---------------- CANCEL ----------------
@login_required
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id, user=request.user)
    appointment.delete()
    return redirect('dashboard')


# ---------------- ABOUT ----------------
def about(request):
    return render(request, 'about.html')


# ---------------- DOCTORS LIST ----------------
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


# ---------------- HOSPITAL LIST ----------------
def hospital_list(request):
    hospitals = Hospital.objects.all()
    return render(request, 'hospitals.html', {'hospitals': hospitals})