from django import forms
from .models import *

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password','role']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','password']

class JobseekerForm(forms.ModelForm):
    class Meta:
        model = JobSeekerModel
        fields = ['resume','bio']
        widgets = {
            'resume' : forms.FileInput(attrs={'class':'form-control'}),
            'bio': forms.TextInput(attrs={'class':'form-control'})
        }

class EmployerForm(forms.ModelForm):
    class Meta:
        model = EmployerModel
        fields = '__all__'
        exclude = ['user']
