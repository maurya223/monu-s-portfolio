from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import messages
from .models import Contact, Feedback, Testimonial


class ModelTestCase(TestCase):
    """Test cases for models"""
    
    def test_contact_model_creation(self):
        """Test Contact model can be created"""
        contact = Contact.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message content'
        )
        self.assertEqual(contact.name, 'Test User')
        self.assertEqual(contact.email, 'test@example.com')
        self.assertEqual(contact.subject, 'Test Subject')
        self.assertEqual(contact.message, 'Test message content')
    
    def test_feedback_model_creation(self):
        """Test Feedback model can be created"""
        feedback = Feedback.objects.create(
            name='Test User',
            email='test@example.com',
            message='Test feedback content'
        )
        self.assertEqual(feedback.name, 'Test User')
        self.assertEqual(feedback.email, 'test@example.com')
        self.assertEqual(feedback.message, 'Test feedback content')
    
    def test_testimonial_model_creation(self):
        """Test Testimonial model can be created"""
        testimonial = Testimonial.objects.create(
            name='Test User',
            position='Developer',
            company='Test Company',
            rating=5,
            message='Great service!',
            is_approved=True
        )
        self.assertEqual(testimonial.name, 'Test User')
        self.assertEqual(testimonial.position, 'Developer')
        self.assertEqual(testimonial.company, 'Test Company')
        self.assertEqual(testimonial.rating, 5)
        self.assertEqual(testimonial.message, 'Great service!')
        self.assertTrue(testimonial.is_approved)
    
    def test_testimonial_default_values(self):
        """Test Testimonial default values"""
        testimonial = Testimonial.objects.create(
            name='Test User',
            message='Test message'
        )
        self.assertEqual(testimonial.rating, 5)
        self.assertFalse(testimonial.is_approved)
        self.assertEqual(testimonial.position, '')
        self.assertEqual(testimonial.company, '')


class ViewTestCase(TestCase):
    """Test cases for views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_view_get(self):
        """Test home view loads correctly"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_view_contact_form_post_valid(self):
        """Test home view handles valid contact form submission"""
        response = self.client.post(reverse('home'), {
            'form_type': 'contact',
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Contact.objects.filter(email='test@example.com').exists())
    
    def test_home_view_contact_form_post_invalid(self):
        """Test home view handles invalid contact form submission"""
        response = self.client.post(reverse('home'), {
            'form_type': 'contact',
            'name': 'Test User',
            'email': 'test@example.com',
            # Missing subject and message
        })
        self.assertEqual(response.status_code, 302)
        # Contact should not be created
        self.assertFalse(Contact.objects.filter(email='test@example.com').exists())
    
    def test_home_view_feedback_form_post_valid(self):
        """Test home view handles valid feedback form submission"""
        response = self.client.post(reverse('home'), {
            'form_type': 'feedback',
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test feedback'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Feedback.objects.filter(email='test@example.com').exists())
    
    def test_home_view_testimonial_form_post_valid(self):
        """Test home view handles valid testimonial form submission"""
        response = self.client.post(reverse('home'), {
            'form_type': 'testimonial',
            'name': 'Test User',
            'message': 'Great service!',
            'rating': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Testimonial.objects.filter(name='Test User').exists())
    
    def test_home_view_displays_approved_testimonials(self):
        """Test home view displays only approved testimonials"""
        # Create approved testimonial
        Testimonial.objects.create(
            name='Approved User',
            message='Approved message',
            is_approved=True
        )
        # Create unapproved testimonial
        Testimonial.objects.create(
            name='Unapproved User',
            message='Unapproved message',
            is_approved=False
        )
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Only approved testimonials should be in context
        self.assertEqual(len(response.context['testimonials']), 1)
        self.assertEqual(response.context['testimonials'][0].name, 'Approved User')
    
    def test_contact_view_get(self):
        """Test contact view loads correctly"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    
    def test_feedback_view_get(self):
        """Test feedback view loads correctly"""
        response = self.client.get(reverse('feedback'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feedback.html')
    
    def test_feedback_view_post_valid(self):
        """Test feedback view handles valid form submission"""
        response = self.client.post(reverse('feedback'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test feedback'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Feedback.objects.filter(email='test@example.com').exists())
    
    def test_feedback_view_post_invalid(self):
        """Test feedback view handles invalid form submission"""
        response = self.client.post(reverse('feedback'), {
            'name': 'Test User',
            # Missing email and message
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Feedback.objects.filter(name='Test User').exists())
    
    def test_about_view_get(self):
        """Test about view loads correctly"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_services_view_get(self):
        """Test services view loads correctly"""
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)
    
    def test_book_appointment_view_get(self):
        """Test book appointment view loads correctly"""
        response = self.client.get(reverse('book-appointment'))
        self.assertEqual(response.status_code, 200)


class URLTestCase(TestCase):
    """Test cases for URL routing"""
    
    def test_home_url(self):
        """Test home URL resolves correctly"""
        url = reverse('home')
        self.assertEqual(url, '/')
    
    def test_contact_url(self):
        """Test contact URL resolves correctly"""
        url = reverse('contact')
        self.assertEqual(url, '/contact/')
    
    def test_feedback_url(self):
        """Test feedback URL resolves correctly"""
        url = reverse('feedback')
        self.assertEqual(url, '/feedback/')
    
    def test_about_url(self):
        """Test about URL resolves correctly"""
        url = reverse('about')
        self.assertEqual(url, '/about/')
    
    def test_services_url(self):
        """Test services URL resolves correctly"""
        url = reverse('services')
        self.assertEqual(url, '/services/')
    
    def test_book_appointment_url(self):
        """Test book appointment URL resolves correctly"""
        url = reverse('book-appointment')
        self.assertEqual(url, '/book-appointment/')

