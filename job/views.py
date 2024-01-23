from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .models import StudentUser, Recruiter, Job, Applicant, Message
from django.contrib import messages


# Create your views here.
@never_cache
def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('user-login')
    # job = Job.objects.all().order_by('-start_date')
    # context = {'job': job}
    return render(request, 'index.html')


@never_cache
def user_joblist(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    jobs = Job.objects.all().order_by('-start_date')

    user = request.user
    student = StudentUser.objects.get(user=user)
    data = Applicant.objects.filter(student=student)
    applied_job_ids = [i.job.id for i in data]
    context = {'jobs': jobs, 'applied_job_ids': applied_job_ids}
    return render(request, 'user/job_list.html', context)


@never_cache
def job_details(request, id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    job = Job.objects.get(id=id)
    context = {'job': job}
    return render(request, 'user/job_details.html', context)


@never_cache
def apply_job(request, id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    job = Job.objects.get(id=id)
    if request.method == "POST":
        resume = request.FILES['resume']
        Applicant.objects.create(job=job, student=student, resume=resume, applydate=date.today())
        messages.success(request, "Congratulations Your Application Was Sent Successfully!")
        return redirect('user-joblist')
    return render(request, 'user/apply_for_job.html')


@never_cache
def show_user_application(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    user = request.user
    data = StudentUser.objects.get(user=user)
    job = Applicant.objects.filter(student=data)
    context = {'job': job}
    return render(request, 'user/my_application.html', context)


@never_cache
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                return redirect('admin-home')
            else:
                messages.error(request, 'You Are Not Admin Brother!')
        except:
            messages.error(request, 'You Are Not Admin Brother!')

    return render(request, 'admin/admin_login.html')


@never_cache
def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    job = Job.objects.select_related('recruiter').all().order_by('-creation_date')

    recruiter = Recruiter.objects.all().count()
    user = StudentUser.objects.all().count()
    context = {'job': job, 'recruiter': recruiter, 'user': user}
    return render(request, 'admin/admin_home.html', context)


@never_cache
def admin_delete_job(request, id):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('admin-home')


@never_cache
def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = StudentUser.objects.all()
    context = {'data': data}
    return render(request, 'admin/view_user.html', context)


@never_cache
def delete_user(request, id):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = User.objects.get(id=id)
    data.delete()
    return redirect('view-users')


@never_cache
def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = Recruiter.objects.filter(status='pending')
    context = {'data': data}
    return render(request, 'admin/recruiter_pending.html', context)


@never_cache
def change_status(request, id):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = Recruiter.objects.get(id=id)
    if request.method == "POST":
        status = request.POST.get('status')
        data.status = status
        try:
            data.save()
            return redirect('recruiter-pending')
        except:
            messages.error(request, "Something Went Wrong !!")

    context = {'data': data}
    return render(request, 'admin/change_status.html', context)


@never_cache
def recruiter_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = Recruiter.objects.filter(status='Accept')
    context = {'data': data}
    return render(request, 'admin/recruiter_accepted.html', context)


@never_cache
def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = Recruiter.objects.filter(status='Reject')
    context = {'data': data}
    return render(request, 'admin/recruiter_rejected.html', context)


@never_cache
def all_recruiter(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = Recruiter.objects.all()
    context = {'data': data}
    return render(request, 'admin/all_recruiter.html', context)


@never_cache
def delete_recruiter(request, id):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    data = User.objects.get(id=id)
    data.delete()
    return redirect('all-recruiter')


def admin_logout(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    logout(request)
    return redirect('admin-login')


# def recruiter_home(request):
#     if not request.user.is_authenticated:
#         return redirect('recruiter-login')
#     return render(request, 'recruiter/recruiter_home.html')

@never_cache
def recruiter_signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        company = request.POST.get('company')
        contact = request.POST.get('contact')
        image = request.FILES['img']
        password = request.POST.get('pass')
        confirm_password = request.POST.get('cpass')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        if not all([firstname, lastname, company, contact, image, password, confirm_password, email, gender]):
            messages.error(request, "Please fill all the required fields")
            return redirect('recruiter-signup')
        if password != confirm_password:
            messages.error(request, "Password and confirm password must be the same")
            return redirect('recruiter-signup')
        try:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            recruiter = Recruiter.objects.create(user=user, mobile=contact, company=company, image=image, gender=gender,
                                                 type="recruiter", status="pending")
            recruiter.save()
            messages.success(request, "Your Account has been created!")
            return redirect('recruiter-login')
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect('recruiter-signup')
    return render(request, 'recruiter/recruiter_signup.html')


@never_cache
def recruiter_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
        print(email, password)
        recruiter = authenticate(username=email, password=password)
        if recruiter:
            try:
                recruiter1 = Recruiter.objects.get(user=recruiter)
                if recruiter1.type == 'recruiter' and recruiter1.status != 'pending' and recruiter1.status != 'Reject':
                    login(request, recruiter)
                    return redirect('recruiter-profile')
                else:
                    messages.error(request, 'Your Login Status is Pendding!')
                    return redirect('recruiter-login')
            except:
                messages.error(request, 'Please enter valid email or password')
                return redirect('recruiter-login')
        else:
            messages.error(request, 'Please enter valid email or password!')
            return redirect('recruiter-login')
    return render(request, 'recruiter/recruiter_login.html')


@never_cache
def add_jobs(request):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        image = request.FILES['img']

        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        job = Job(recruiter=recruiter, title=title, description=description, skills=skills,
                  location=location, salary=salary, experience=experience, start_date=start_date,
                  end_date=end_date, image=image)
        job.save()
        messages.success(request, 'New Job Added')
        return redirect('job-list')
    return render(request, 'recruiter/add_jobs.html')


@never_cache
def job_list(request):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    data = Job.objects.filter(recruiter=recruiter).order_by('-creation_date')
    context = {'data': data}
    return render(request, 'recruiter/job_list.html', context)


@never_cache
def update_job(request, myid):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    update = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # image = request.POST.get('img')

        update.title = title
        update.description = description
        update.skills = skills
        update.location = location
        update.salary = salary
        update.experience = experience
        update.start_date = start_date
        update.end_date = end_date
        update.save()
        messages.success(request, "Job Details has been Updated")
        return redirect('job-list')
    context = {'update': update}
    return render(request, 'recruiter/update_jobdetails.html', context)


@never_cache
def delete_job(request, id):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    job = Job.objects.get(id=id)
    job.delete()
    return redirect('job-list')


@never_cache
def recruiter_profile(request):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    user = request.user
    data = Recruiter.objects.get(user=user)
    context = {'data': data}
    return render(request, 'recruiter/recruiter_profile.html', context)


@never_cache
def update_recruiter(request, id):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    data = Recruiter.objects.get(id=id)
    # user = User.objects.get(id=id)

    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        company = request.POST.get('company')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        img = request.FILES['img']

        request.user.first_name = first_name
        request.user.last_name = last_name
        data.company = company
        data.contact = contact
        request.user.username = email
        data.gener = gender
        data.image = img
        request.user.save()
        data.save()
        return redirect('recruiter-profile')
    context = {'data': data}
    return render(request, 'recruiter/update_recruiter.html', context)


@never_cache
def show_apply_candidate(request):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    data = Applicant.objects.all()
    context = {'data': data}
    return render(request, 'recruiter/applied_candidate.html', context)


@never_cache
def delete_candidate(request, id):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    candidate = Applicant.objects.get(id=id)
    candidate.delete()
    return redirect('show-apply-candidate')


@never_cache
def user_signup(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        contact = request.POST.get('contact')
        image = request.FILES['img']
        password = request.POST.get('pass')
        confirm_password = request.POST.get('cpass')
        email = request.POST.get('email')
        gender = request.POST.get('gender')

        if not all([firstname, lastname, contact, image, password, confirm_password, email, gender]):
            messages.error(request, "Please fill all the required fields")
            return redirect('user-signup')
        if password != confirm_password:
            messages.error(request, "Password and confirm password must be the same")
            return redirect('user-signup')
        try:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=email, password=password)
            studentusers = StudentUser.objects.create(user=user, mobile=contact, image=image, gender=gender,
                                                      type="student")
            studentusers.save()
            messages.success(request, "Your Account has been created!")
            return redirect('user-login')
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect('user-signup')
    return render(request, 'user/user_signup.html')


@never_cache
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            try:
                user1 = StudentUser.objects.get(user=user)
                if user1.type == 'student':
                    login(request, user)
                    return redirect('user-joblist')
                else:
                    messages.error(request, 'Please enter valid email or password!')
                    return redirect('user-login')
            except:
                pass
        else:
            messages.success(request, 'Please enter valid email or password!')
            return redirect('user-login')
    return render(request, 'user/user_login.html')


@never_cache
def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    user = request.user
    data = StudentUser.objects.get(user=user)
    context = {'data': data}
    return render(request, 'user/user_profile.html', context)


@never_cache
def user_update(request, id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    data = StudentUser.objects.get(id=id)
    if request.method == "POST":
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')
        img = request.FILES['img']

        request.user.first_name = first_name
        request.user.last_name = last_name
        data.contact = contact
        data.gender = gender
        data.image = img
        request.user.save()
        data.save()
        messages.success(request, 'Your Profile Has Been Updated')
        return redirect('user-profile')
    context = {'data': data}
    return render(request, 'user/user_update.html', context)


@never_cache
def job_search(request):
    if not request.user.is_authenticated:
        return redirect('user-login')
    query = request.GET.get('search')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        messages.error(request, 'Jobs Not Found')
        return redirect('user-joblist')
    context = {'jobs': jobs}
    return render(request, 'user/job_list.html', context)


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user-login')


@never_cache
def send_message(request, job_id):
    if not request.user.is_authenticated:
        return redirect('user-login')
    job = Job.objects.get(id=job_id)
    if request.method == "POST":
        content = request.POST.get('content')
        recipient = job.recruiter.user
        message = Message.objects.create(sender=request.user, recipient=recipient, job=job, content=content)
        messages.success(request, "Your Message has been sent...!")
        return redirect('user-joblist')
    else:
        pass
    return render(request, 'user/send_message.html', {'job': job})


@never_cache
def job_messages(request, job_id):
    if not request.user.is_authenticated:
        return redirect('recruiter-login')
    job = Job.objects.get(id=job_id)
    msg = Message.objects.filter(job=job).order_by('-timestamp')
    return render(request, 'recruiter/job_message.html', {'job': job, 'msg': msg})