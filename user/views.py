from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,authenticate,logout
from .models import CustomUser 
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime



# Create your views here.
def about(request):
    return render(request, 'about.html')
def mainuser(request):
    return render(request,"user.html")


@login_required
def seekerpro(request):
    user = request.user  # Get the logged-in user

    # ✅ Get or create a Seeker profile
    seeker_profile, created = SeekerProfile.objects.get_or_create(user_connected=user)

    if request.method == 'POST':
        seeker_profile.name = request.POST.get('sname', '').strip()
        seeker_profile.address = request.POST.get('addr', '').strip()
        seeker_profile.phone_number = request.POST.get('sp', '').strip()
        seeker_profile.email = request.POST.get('em', '').strip()
        seeker_profile.gender = request.POST.get('gen', '').strip()

        # ✅ Handle Image Upload Properly
       
        seeker_profile.image = request.FILES.get('image') # Correct way to handle file uploads

        try:
            seeker_profile.save()  # ✅ Save updated profile
            messages.success(request, "Profile updated successfully!")
            print("Seeker profile updated successfully:", seeker_profile)
            return render(request, 'home.html', {'success': 'Profile updated successfully!'})
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")
            print("Error updating SeekerProfile:", e)

    return render(request, 'seeker.html', {'profile': seeker_profile})

def home(request):
    return render(request, 'home.html')

@login_required
def creatorpro(request):
    user = request.user  

    # ✅ Check if profile exists, don't create a new one
    creator_profile = CreatorProfile.objects.filter(user_connected=user).first()

    if not creator_profile:  # If no profile exists, create one
        creator_profile = CreatorProfile.objects.create(user_connected=user)

    if request.method == 'POST':
        creator_profile.name = request.POST.get('cname', '').strip()
        creator_profile.address = request.POST.get('add', '').strip()
        creator_profile.phone_number = request.POST.get('p', '').strip()
        creator_profile.em = request.POST.get('e', '').strip()
        creator_profile.companyname = request.POST.get('cn', '').strip()
        creator_profile.yofex = int(request.POST.get('expe', 0))  # Convert to integer
        creator_profile.gender = request.POST.get('gen', '').strip()
        creator_profile.save()  # ✅ Save the updated values

        print("Updated creator profile:", creator_profile)

        return render(request, 'home.html', {'success': 'Profile updated successfully!'})

    return render(request, 'creator.html', {'profile': creator_profile})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')

        
            # ✅ Use session variable set by signal
            redirect_to = request.session.pop('redirect_to', None)
            if redirect_to:
                return redirect(redirect_to)

            return redirect('home')  # Default redirect if session doesn't work
        else:
            return redirect('r') 

    return render(request, "login.html")




@csrf_exempt
def register(request):
    if request.method == "POST":
        # Your registration logic here
        return HttpResponse("Registration Successful")



def register(request):
    if request.method == 'POST':
        username = request.POST.get('u_name', '').strip()
        password = request.POST.get('pwd', '').strip()
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        role = request.POST.get('r', '').strip()

        # ✅ Check if username already exists before creating a new user
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different one.")
            return render(request, 'register.html')

        # ✅ Create the user
        user = CustomUser.objects.create_user(
            username=username, 
            password=password, 
            fi=fname,  
            ln=lname,  
            user_type=role
        )
        user.is_staff = True
        user.save()

        print(f"User '{user.username}' has been created with user_type: '{user.user_type}'")

        # ✅ Log in the user after registration
        login(request, user)

        # ✅ Create profile only if it doesn't exist
        if role == 'Creator':
            CreatorProfile.objects.get_or_create(user_connected=user)
            return redirect('cp')  # Redirect to Creator Profile
        elif role == 'Seeker':
            SeekerProfile.objects.get_or_create(user_connected=user)
            return redirect('sp')  # Redirect to Seeker Profile
        else:
            return redirect('home')  # Default redirect if user type is unknown

    return render(request, 'register.html')




@login_required
def addjob(request):
    if request.method == 'POST':
        print("🔹 Job POST request received!")  # ✅ Confirm POST request

        # ✅ Debug: Check if POST data is received
        print("Received POST data:", request.POST)

        comname = request.POST.get('comname', '').strip()
        jtitle = request.POST.get('jobtitle', '').strip()
        sdate = request.POST.get('sdate', '').strip()
        edate = request.POST.get('edate', '').strip()
        salary = request.POST.get('Salary', '').strip()
        ex = request.POST.get('Exp', '').strip()
        lo = request.POST.get('lo', '').strip()
        skills = request.POST.get('sk', '').strip()
        des = request.POST.get('de', '').strip()

        # ✅ Fix CreatorProfile retrieval
        try:
            creator = get_object_or_404(CreatorProfile, user_connected=request.user)
            print("✅ Creator Profile Found:", creator)
        except Exception as e:
            print(" Error fetching CreatorProfile:", e)
            return render(request, "addjob.html", {"error": "Creator Profile not found!"})

        try:
            salary = float(salary) if salary else 0.0
            ex = int(ex) if ex.isdigit() else 0
            sdate = datetime.strptime(sdate, "%Y-%m-%d").date() if sdate else None
            edate = datetime.strptime(edate, "%Y-%m-%d").date() if edate else None

            # ✅ Use `user_connected` instead of `creator`
            job = JobAdd.objects.create(
                user_connected=request.user,  # ✅ Fixed field
                company_name=comname,
                job_title=jtitle,
                sdate=sdate,
                edate=edate,
                salary=salary,
                experience=ex,
                location=lo,
                skills=skills,
                descri=des
            )

            job.save()
            print("✅ Job saved successfully:", job)

            # ✅ Redirect after successful job posting
            return redirect('jl')  # Redirect to job list

        except Exception as e:
            print(" Error adding job:", e)

    return render(request, "addjob.html")


def creator_profile(request):
    username = request.GET.get('username')  # Retrieve from query parameters
    if not username:
        return render(request, 'error.html', {'message': 'Username is required'})

    creator = get_object_or_404(CreatorProfile, user_connected__username=username)
    return render(request, 'creator_view.html', {'creator': creator})

def joblist(request):
    
    data=JobAdd.objects.all()
    
    d={'data':data}
    return render(request,"joblist.html",d)
@login_required
def creatordas(request,username) :
    creator = get_object_or_404(CreatorProfile, user_connected__username=username)
    return render(request,"cdasboard.html", {'creator': creator})
@login_required 
def seekerdas(request,username) :
    seeker = get_object_or_404(SeekerProfile, user_connected__username=username)
    applied_jobs = JobApplication.objects.filter(seeker=seeker)
    return render(request,"sdasboard.html",{'seeker': seeker,'applied_jobs': applied_jobs})   


def seeker_profile(request):
    username = request.GET.get('username')  # Retrieve from query parameters
    if not username:
        return render(request, 'error.html', {'message': 'Username is required'})

    seeker = get_object_or_404(SeekerProfile, user_connected__username=username)
    return render(request, 'seeker_view.html', {'seeker': seeker})
def logout_view(request):
    logout(request)
    return redirect('l') 
  

def seeker_login(request, job_id):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user and user.user_type == "Seeker":  # Sirf Seeker login kar sake
            login(request, user)
            return redirect(f"/apply-form/{job_id}/")  # Apply form per redirect karein
        else:
            messages.error(request, "Invalid credentials or you are not a Seeker!")

    return render(request, "seeker_login.html", {"job_id": job_id})


@login_required  # Ensure user is logged in before applying
def apply_form(request, job_id):
    job = get_object_or_404(JobAdd, id=job_id)  # ✅ Ensures job exists

    try:
        seeker_profile = get_object_or_404(SeekerProfile, user_connected=request.user)  # ✅ Ensures seeker profile exists
    except:
        return redirect("/seeker-profile-create/")  # 🔹 If seeker profile doesn't exist, ask to create one

    if request.method == "POST":
        resume = request.FILES.get("resume")

        # ✅ Check if application already exists
        if JobApplication.objects.filter(job=job, seeker=seeker_profile).exists():
            return render(request, "apply.html", {
                "job": job,
                "seeker_profile": seeker_profile,
                "error": "You have already applied for this job!",
            })

        # ✅ Save the Job Application
        JobApplication.objects.create(
            job=job,
            seeker=seeker_profile,
            resume=resume
        )
        return redirect('jl')  # ✅ Redirect back to job list after applying

    return render(request, "apply.html", {"job": job, "seeker_profile": seeker_profile})


@login_required
def showjob(request):
    # Get the logged-in user (Creator)
    logged_in_creator = request.user

    # Filter job applications where the job was created by the logged-in creator
    data = JobApplication.objects.filter(job__user_connected=logged_in_creator)

    return render(request, "showjob.html", {'data': data})


def approve_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)

    # Get the username of the job creator
    creator_username = application.job.user_connected.username  

    # Update application status
    application.status = "Approved"  # Ensure the model has a 'status' field
    application.save()

    # Show success message
    messages.success(request, "Application approved successfully.")

    # Redirect to creator's dashboard using username
    return redirect('cdas', username=creator_username)


def reject_application(request, application_id):
    try:
        # Get the job application
        application = get_object_or_404(JobApplication, id=application_id)

        # Get the username of the job creator (since URL expects 'username')
        creator_username = application.job.user_connected.username  

        # Delete the application
        application.delete()

        # Show success message
        messages.success(request, "Application rejected and deleted.")

        # Redirect to creator dashboard using username
        return redirect('cdas', username=creator_username)

    except JobApplication.DoesNotExist:
        messages.error(request, "The requested application does not exist.")
        return redirect('sj')  # Redirect to job applications page if not found

def showapplyjob(request, username):
    # Get the seeker based on the username
    seeker = get_object_or_404(SeekerProfile, user_connected__username=username)
    
    # Fetch all job applications for this seeker
    applied_jobs = JobApplication.objects.filter(seeker=seeker)

    # Render the template with applied jobs data
    return render(request, 'showapplyjob.html', {'seeker': seeker, 'applied_jobs': applied_jobs})

def apanel(request):
    return render(request,"apanel.html")    
def allseeker(request):
    data=SeekerProfile.objects.all()
    
    d={'data':data}
    return render(request,"allseekers.html",d)
def allcreator(request):
    data=CreatorProfile.objects.all()
    d={'data':data}
    return render(request,"allcreators.html",d)
def allapplyjob(request):
    data=JobApplication.objects.all()
    d={'data':data}
    return render(request,"allapplyjob.html",d)
def delete_seeker(request, seeker_id):
    seeker = get_object_or_404(SeekerProfile, id=seeker_id)
    seeker.delete()
    return redirect('alls') 
def delete_creator(request, creator_id):
    creator = get_object_or_404(CreatorProfile, id=creator_id)
    creator.delete()
    return redirect('allc') 
def contact(request):
    return render(request,"contact.html")