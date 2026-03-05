from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_view, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
]
