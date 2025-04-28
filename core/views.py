from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .forms import *
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login

class Register(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name ='register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        raw_password = form.cleaned_data.get('password')
        user.set_password(raw_password)
        user.save()
        return super().form_valid(form)
    
def home(request):
    return HttpResponse('You are welcome')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})

    return render(request, 'login.html')

def jobseekerhomepage(request):
    data = EmployerModel.objects.all()
    context = {'employerdata':data}
    return render(request,'jobseeker.html',context)

def jobseeker_applicationpage(request,pk):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = JobseekerForm(request.POST, request.FILES)
            if form.is_valid():

                user = form.save(commit=False)
                user_pk = request.user
                user.user = user_pk
                user.save()
            else:
                data = EmployerModel.objects.get(id=pk)
                context = {'employerinfo':data,
                'form':form}
                return render(request,'apply_page.html',context)
        data = EmployerModel.objects.get(id=pk)
        context = {'employerinfo':data,
                'form':JobseekerForm()}
        return render(request,'apply_page.html',context)
    return redirect('login')

def employer(request):
    employer_instance = EmployerModel.objects.get(user=request.user)
    jobseekers = JobSeekerModel.objects.filter(job=employer_instance)  # Filter by Employer
    context = {'jobseekers': jobseekers, 'employer_instance': employer_instance}
    return render(request, 'employer.html', context)

### fix employer page this isnt really working beacause logic mileko xaina do it all over again