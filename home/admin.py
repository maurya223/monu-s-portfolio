from django.contrib import admin
from .models import Contact, Feedback, Project, Testimonial

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('email',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')
    list_filter = ('email',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'is_approved', 'created_at')
    search_fields = ('name', 'company', 'message')
    list_filter = ('is_approved', 'rating', 'created_at')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)

