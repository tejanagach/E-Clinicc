from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('home/', views.home, name='home'),
    path('upload/', views.upload_details, name='upload_details'),
    path('history/', views.history, name='history'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('medicine_reminders/', views.medicine_reminders, name='medicine_reminders'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.about_us, name='about_us'),
    path('my_profile/', views.my_profile, name='my_profile'),
]
