from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('book/<int:doctor_id>/', views.book_appointment, name='book'),
    path('appointments/', views.appointments, name='appointments'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('approve/<int:id>/', views.approve_appointment, name='approve'),
    path('reject/<int:id>/', views.reject_appointment, name='reject'),
    path('cancel/<int:id>/', views.cancel_appointment, name='cancel'),

    path('about/', views.about, name='about'),
    path('doctors/', views.doctor_list, name='doctors'),
    path('hospitals/', views.hospital_list, name='hospitals'),
]