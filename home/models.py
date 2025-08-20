from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  
    subject = models.CharField(max_length=200)
    # this is required field
    message = models.TextField()

    
class Project(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="projects/")

    def __str__(self):
        return self.title

# feedback form 
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()  # ✅ Add this
    # this is required field
    message = models.TextField()

   