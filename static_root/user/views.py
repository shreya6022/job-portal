from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login,authenticate
from .models import CustomUser 
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def mainuser(request):
    return render(request,"user.html")
def seekerpro(request):
    if request.method == 'POST':
        username = request.POST.get('sun', '').strip()
        password = request.POST.get('spw', '').strip()
        name = request.POST.get('sname', '').strip()
        add = request.POST.get('addr', '').strip()
        f = request.POST.get('sfn', '').strip()
        l = request.POST.get('sln', '').strip()
        ph = request.POST.get('sp', '').strip()
        role = request.POST.get('sro', '').strip()
        emails = request.POST.get('em', '').strip()
        image = request.POST.get('im', '').strip()
        ge = request.POST.get('gen', '').strip()
        try:
             en=CustomUser.objects.create_user(username=username,password=password,fi=f,ln=l,user_type=role)
             s=SeekerProfile.objects.create(user_connected=en,
             email=emails,gender=ge,image=image,name=name,address=add,phone_number=ph)
             s.save()
             print("Seeker profile saved successfully:", s)
        except Exception as e:
             print("Error saving seekerProfile:", e) 

    return render(request, 'seeker.html')
def home(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            return redirect('l')  # Replace 'login_view' with your actual login view name
        elif action == 'regi':
            return redirect('r')  #
    return render(request, 'home.html')
def creatorpro(request):
    if request.method == 'POST':
        username = request.POST.get('un', '').strip()
        password = request.POST.get('pw', '').strip()
        name = request.POST.get('cname', '').strip()
        add = request.POST.get('add', '').strip()
        f = request.POST.get('fn', '').strip()
        l = request.POST.get('ln', '').strip()
        ph = request.POST.get('p', '').strip()
        role = request.POST.get('ro', '').strip()
        try:
             en=CustomUser.objects.create_user(username=username,password=password,fi=f,ln=l,user_type=role)
             c=CreatorProfile.objects.create(user_connected=en,name=name,address=add,phone_number=ph)
             c.save()
             print("creator profile saved successfully:", c)
        except Exception as e:
             print("Error saving CreatorProfile:", e) 

    return render(request, 'creator.html')



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
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

@csrf_exempt
def register(request):
    if request.method == "POST":
        # Your registration logic here
        return HttpResponse("Registration Successful")
    
def register(request):
    error=" "
    if request.method == 'POST':
        username = request.POST.get('u_name', '').strip()
        password = request.POST.get('pwd', '').strip()
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        role = request.POST.get('r', '').strip()

        # ✅ Check if username already exists **before creating the user**
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose a different one.")
            return render(request, 'register.html')
        
        # ✅ Create new user
        user = CustomUser.objects.create_user(username=username, password=password)
        user.fi = fname
        user.ln = lname
        user.user_type = role
        user.is_staff = True
        
        user.save()
        print(f"User '{user.username}' has been created with user_type: '{user.user_type}'")
        # ✅ Correct login usage
        login(request, user)
        return redirect('l')  
    return render(request, 'register.html')
def creatorview(request):
    return render(request,"creator_view.html")
def addjob(request):
    return render(request,"addjob.html")
def seekerview(request):
    data=SeekerProfile.objects.all()
    d={'data':data}
    return render(request,"seeker_view.html",d)
