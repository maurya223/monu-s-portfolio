from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Contact


def home(request):
    """Home page + contact form submission."""
    if request.method == 'POST' and request.POST.get('form_type') == 'contact':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )

            # Send email
            try:
                send_mail(
                    subject=f"New Contact Message: {subject}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['mauryaharshit376@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully')
            except Exception as e:
                messages.warning(request, f'Message saved, but email failed to send: {e}')

            return redirect('home')

        messages.error(request, 'All contact fields are required')
        return redirect('home')

    return render(request, 'home.html')


def contact_form(request):
    """Legacy endpoint; keeps the existing URL working if used elsewhere."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
            )

            send_mail(
                subject,
                f"Message from {name} ({email}):\n\n{message}",
                email,
                ["mauryaharshit376@gmail.com"],
                fail_silently=False,
            )

            return HttpResponse('Thank you for your message!')

        return HttpResponse('All fields are required', status=400)

    return render(request, 'contact.html')


def about_view(request):
    """Display about page"""
    return render(request, 'about.html')


def services_view(request):
    """Display services page"""
    return render(request, 'services.html')

