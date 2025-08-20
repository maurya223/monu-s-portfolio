
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, Feedback

def home(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'contact':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            if name and email and subject and message:
                contact = Contact(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message
                )
                contact.save()  # Explicit save()

                # Send email
                try:
                    send_mail(
                        subject=f"New Contact Message: {subject}",
                        message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=['maurya892096@gmail.com'],
                        fail_silently=False,
                    )
                    messages.success(request, 'Your message has been sent successfully')
                except Exception as e:
                    messages.warning(request, f'Message saved, but email failed to send: {e}')

                return redirect('home')
            else:
                messages.error(request, 'All contact fields are required')

        elif form_type == 'feedback':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            if name and email and message:
                feedback = Feedback(
                    name=name,
                    email=email,
                    message=message
                )
                feedback.save()  # Explicit save()

                messages.success(request, 'Your feedback has been submitted successfully')
                return redirect('home')
            else:
                messages.error(request, 'All feedback fields are required')

    return render(request, 'home.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Message from {name} ({email}):\n\n{message}"

        # Send email
        send_mail(
            subject,                # subject from user
            full_message,           # message body
            email,                  # from user
            ["mauryaharshit376@gmail.com"],    # recipient list
            fail_silently=False
        )

        return HttpResponse('Thank you for your message!')

    # For GET request, render the form
    return render(request, 'contact.html')

def feedback_view(request):
    """Handle feedback form submissions"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if name and email and message:
            feedback = Feedback(
                name=name,
                email=email,
                message=message
            )
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully')
            return redirect('feedback')
        else:
            messages.error(request, 'All fields are required')

    return render(request, 'feedback.html')

def book_appointment(request):
    """Handle appointment booking"""
    if request.method == 'POST':
        # Add appointment booking logic here
        messages.success(request, 'Appointment booked successfully!')
        return redirect('book-appointment')
    
    return render(request, 'book_appointment.html')

def about_view(request):
    """Display about page"""
    return render(request, 'about.html')

def services_view(request):
    """Display services page"""
    return render(request, 'services.html')