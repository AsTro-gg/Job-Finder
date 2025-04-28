from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employer','Employer'),
        ('job_seeker',('Job_seeker'))
    ]

    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30,choices=ROLE_CHOICES)

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username
    
class EmployerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=300)
    website = models.URLField(blank=True , null=True)
    company_logo = models.ImageField(upload_to='company/')
    recruitment_requirements = models.TextField(max_length=50)
    post = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.post} created by {self.user}"
    
class JobSeekerModel(models.Model):
    job = models.ForeignKey(EmployerModel,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/')
    bio = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def delete(self):
        self.resume.delete()
        super().delete()


    def __str__(self):
        return f"{self.user} as Job Seeker"

class AppliedTo(models.Model):
    STATUS_CHOICES = [
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('pending','Pending') 
    ]
    post = models.ForeignKey(EmployerModel,on_delete=models.CASCADE)
    applied_by = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"{self.post} applied by {self.applied_by}"