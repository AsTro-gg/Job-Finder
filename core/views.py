from django.shortcuts import render,HttpResponse,redirect
from .models import *
from .forms import *
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import Group

class Register(generic.CreateView):
    model = User
    form_class = UserRegisterForm
    template_name ='register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        group,_ = Group.objects.get_or_create(name = user.role)
        
        raw_password = form.cleaned_data.get('password')
        user.set_password(raw_password)
        user.save()
        user.groups.add(group)
        return super().form_valid(form)
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is not None:
            print(f"User {user} authenticated successfully.") 
            login(request, user)
            if user.groups.filter(name='employer').exists():  # Check if the user is in the 'Employer' group
                return redirect('employer')
            else:
                return redirect('jobseeker')
        else:
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})

    return render(request, 'login.html')


def jobseekerhomepage(request):
    if request.user.role == 'job_seeker':
        data = EmployerModel.objects.all()
        context = {'employerdata':data}
        return render(request,'jobseeker.html',context)
    return redirect('login')

def jobseeker_applicationpage(request, pk):
    if request.user.is_authenticated:
        if request.user.role == 'job_seeker':
        
            if request.method == 'POST':
                form = JobseekerForm(request.POST, request.FILES)
                if form.is_valid():
                    # Check if the user has already applied for this job
                    employer = EmployerModel.objects.get(id=pk)
                    existing_application = JobSeekerModel.objects.filter(user=request.user, job=employer).first()

                    if existing_application:
                        # If the user has already applied, you can update the existing application
                        # Alternatively, you can redirect or show a message that the user has already applied
                        return redirect('jobseeker')  # Replace with the actual URL name of the "already applied" page

                    # Create a new application if no previous application exists
                    user = form.save(commit=False)
                    user.user = request.user  # Assign the logged-in user
                    user.job = employer  # Assign the employer (job) to the user
                    user.save()

                    # Redirect to a success or confirmation page
                    return redirect('jobseeker')  # Replace with the actual URL name for success page
                else:
                    # If the form is invalid, re-render the form with the current context
                    data = EmployerModel.objects.get(id=pk)
                    context = {'employerinfo': data, 'form': form}
                    return render(request, 'apply_page.html', context)

            # If the request method is GET, show the form to apply
            data = EmployerModel.objects.get(id=pk)
            context = {'employerinfo': data, 'form': JobseekerForm()}
            return render(request, 'apply_page.html', context)
        return redirect('login')

    # If the user is not authenticated, redirect to the login page
    return redirect('login')

def employer(request):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            employer_instance = EmployerModel.objects.filter(user=request.user)
            post_count = employer_instance.count()
            applied_count = AppliedTo.objects.filter(post__user=request.user).count()
            accepted_count = AppliedTo.objects.filter(post__user = request.user,status = 'accepted').count()
            rejected_count = AppliedTo.objects.filter(post__user = request.user,status = 'rejected').count()
            pending_count = AppliedTo.objects.filter(post__user = request.user,status = 'pending').count()

            context = {
                'employer_instance': employer_instance,
                'post': post_count,
                'applied_by': applied_count,
                'accepted':accepted_count,
                'rejected':rejected_count,
                'pending':pending_count,
                        }
            return render(request, 'employer.html', context)
        return redirect('login')
    return redirect('login')

def ViewApplication(request, pk):
    if request.user.is_authenticated:
        if request.user.role == 'employer':
            post = EmployerModel.objects.get(id=pk)
            job_applications = JobSeekerModel.objects.filter(job=post)
            
            # Create a list to store job applications with their respective resume_is_image flag
            applications_with_resumes = []
            for application in job_applications:
                # Check if the resume is an image
                if application.resume:
                    resume_is_image = application.resume.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
                else:
                    resume_is_image = False
                
                # Add to the list with both the application and resume_is_image flag
                applications_with_resumes.append({
                    'application': application,
                    'resume_is_image': resume_is_image
                })
        
            # Pass the data to the context
            context = {'list': post, 'applications_with_resumes': applications_with_resumes}
            return render(request, 'view_application.html', context)
        return redirect('login')
    return redirect('login')

def CreateVacancies(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)  # Ensure files are included
        if form.is_valid():
            # Form is valid, save the data
            user = form.save(commit=False)
            user.user = request.user  # Assign the logged-in user
            user.save()  # Save the form data

            # Redirect to the employer dashboard or another success page
            return redirect('employer')
        else:
            # Print form errors for debugging
            print(form.errors)  # Logs errors in the server console
            context = {'form': form}
            return render(request, 'create_vacancies.html', context)
    
    # GET request
    context = {'form': EmployerForm()}
    return render(request, 'create_vacancies.html', context)

