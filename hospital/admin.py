from django.contrib import admin
from .models import Doctor, DoctorAvailability, Appointment, Hospital


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'experience', 'fee', 'rating')


class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day', 'available_from', 'available_to')


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient_name', 'doctor__name')


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Doctor, DoctorAdmin)
admin.site.register(DoctorAvailability, DoctorAvailabilityAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Hospital, HospitalAdmin)