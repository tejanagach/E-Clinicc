# views.py
from django.contrib.auth import login, authenticate, logout  # Import the 'logout' function
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserDetails, MedicineReminder
from django.utils import timezone

def base(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect login credentials. Please try again.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user, created = User.objects.get_or_create(username=email)
        if not created:
            messages.error(request, 'This user already exists. Please choose a different email.')
            return render(request, 'signup.html')
        user.set_password(password)
        user.save()
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'signup.html')

def home(request):
    return render(request, 'home.html')

def upload_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        hospital_name = request.POST.get('hospital_name', 'No Name')
        hospital_address = request.POST.get('hospital_address', 'No Address')
        doctor_name = request.POST.get('doctor_name', 'No Name')
        disease = request.POST.get('disease', 'No Disease')
        fees = request.POST.get('fees', 0)
        image_type = request.POST.get('image_type', 'Other')
        date = request.POST.get('date', timezone.now())
        image = request.FILES.get('image')

        if name and email and image:
            UserDetails.objects.create(
                name=name,
                email=email,
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                doctor_name=doctor_name,
                disease=disease,
                fees=fees,
                image_type=image_type,
                date=date,
                image=image,
                user=request.user
            )
            return redirect('history')
        else:
            # Handle invalid form data, e.g., show an error message
            pass

    return render(request, 'upload_details.html')

@login_required
def history(request):
    details = UserDetails.objects.filter(user=request.user).order_by('-date')
    return render(request, 'history.html', {'details': details})

@login_required
def medicine_reminders(request):
    if request.method == 'POST':
        medicine_name = request.POST.get('medicine_name')
        quantity = request.POST.get('quantity')
        reminder_datetime = request.POST.get('reminder_datetime')

        MedicineReminder.objects.create(
            user=request.user,
            medicine_name=medicine_name,
            quantity=quantity,
            reminder_datetime=reminder_datetime
        )
        return redirect('medicine_reminders')

    reminders = MedicineReminder.objects.filter(user=request.user)
    return render(request, 'medicine_reminders.html', {'reminders': reminders})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import render

def about_us(request):
    return render(request, 'about.html')
from django.shortcuts import render

def my_profile(request):

    user_details = {
        'name': 'Your Name',
        'email': 'your.email@example.com',
        'phone': '+1 234 567 890',
        'address': 'Your Address, City, Country',
        'profile_picture': '../static/img/profile_picture.jpg',  # Update with the actual path
    }

    return render(request, 'my_profile.html', {'user_details': user_details})

