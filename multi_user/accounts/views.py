from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm, RegisterForm, BlogCreation,AppointmentCreation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import MyUser, Blog, Appointment
from unicodedata import category
from django.db.models import Q

from django.shortcuts import render

from datetime import datetime, timedelta
import pickle
from googleapiclient.discovery  import build
from google_auth_oauthlib.flow import InstalledAppFlow
# from apiclient.discovery import build 
# from googleapiclient.discovery import build

# from google_auth_oauthlib.flow import InstalledAppFlow

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# Create your views here.



def register_page(request):
	forms=RegisterForm()
	if request.method=='POST':
		form=RegisterForm(request.POST, request.FILES)
		if form.is_valid():
			obj=form.save(commit=False)
			obj.save()
			return redirect('login')
	else:
		return render(request, 'accounts/register_page.html', {'form':forms})
    

def login_page(request):
	if request.user.is_authenticated:
		return redirect('profile')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('profile')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login_page.html', context)

@login_required(login_url='login')
def profile_page(request):
    data=MyUser.objects.all()
    return render(request, 'accounts/profile_page.html', {'datas':data})

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def blogs(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def drafts(request):
    data = Blog.objects.filter(is_draft=True, myuser=request.user)
    return render(request, 'myblog/draft_1.html', {'data': data})

@login_required(login_url='login')
def myblogs(request):
    data = Blog.objects.filter(myuser=request.user, is_draft=False)
    return render(request, 'myblog/myblogs_1.html', {'data': data})

@login_required(login_url='login')
def createBlog(request):
    if request.method == 'POST':
        form = BlogCreation(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            user = request.user
            blog_category = form.cleaned_data['blog_category']
            summary = form.cleaned_data['summary']
            content = form.cleaned_data['content']
            is_draft = form.cleaned_data['is_draft']
            blog_image=request.FILES.get('blog_image')
            blog = Blog(
                myuser=user, title=title, blog_category=blog_category, summary=summary, content=content, is_draft=is_draft, blog_image=blog_image)
            blog.save()
            
            if(is_draft == False):
                messages.success(
                    request, 'Your Blog has been Successfully Created')
                return redirect('myblogs')
            else:
                messages.success(
                    request, 'Your Draft has been Successfully Created')
                return redirect('drafts')
        else:
            msg = 'Try Again!'
            return render(request, 'myblog/createblog.html', {'form': form, 'msg': msg})
    else:
        form = BlogCreation()
        return render(request, 'myblog/createblog.html', {'form': form})

@login_required(login_url='login')
def blogsall(request):
    data = Blog.objects.filter(is_draft=False)
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def mhealth(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Mental Health')
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def heartdis(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Heart Disease')
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def covid19(request):
    data = Blog.objects.filter(is_draft=False, blog_category='COVID19')
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def immun(request):
    data = Blog.objects.filter(is_draft=False, blog_category='Immunization')
    return render(request, 'myblog/blogs_1.html', {'data': data})

@login_required(login_url='login')
def appointment(request):
    data = MyUser.objects.filter(doctor=True)
    return render(request, 'appointment/appointment_1.html', {'data': data})

@login_required(login_url='login')
def create_appoint(request, pk):
    doctor = MyUser.objects.get(Q(pk=pk))
    first_name = doctor.first_name
    last_name = doctor.last_name
    full_name = str(first_name) + " " + str(last_name)
    if request.method == 'POST':
        form = AppointmentCreation(request.POST)
        if form.is_valid():
            app_date = form.cleaned_data['app_date']
            location = doctor.city
            user = request.user
            docof = MyUser.objects.get(Q(username=doctor.username))
            app_time = form.cleaned_data['app_time']
            speciality = form.cleaned_data['speciality']
            end_time = calendar_app(full_name, app_date, app_time, location)
            print(type(end_time))
            appoint = Appointment(
                doctor_name=docof, patient_name=user, app_date=app_date, app_time=app_time, speciality=speciality, end_time=end_time)
            appoint.save()
            messages.success(
                request, 'Your Appointment has been scheduled')
            data = Appointment.objects.filter(patient_name=request.user)
            return render(request, 'appointment/viewappoint_1.html', {'data': data})
        else:
            msg = 'Errors while validating the form. Try Again!'
            return render(request, 'appointment/appointform.html', {'form': form, 'msg': msg})
    else:
        form = AppointmentCreation()
        return render(request, 'appointment/appointform.html', {'form': form, 'doctor': full_name})


def calendar_app(doctor, dateof, timeof, city):
    scopes = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file(
        "accounts\client_secret.json", scopes=scopes)
    # credentials = flow.run_console()
    # pickle.dump(credentials, open("token.pkl", "wb"))

    credentials = pickle.load(open("token.pkl", "rb"))
    
    service = build("calendar", "v3", credentials=credentials)
   
    result = service.calendarList().list().execute()
    calendar_id = result['items'][1]['id']
    result = service.events().list(calendarId=calendar_id).execute()

    date_of = dateof.strftime("%d")
    month_of = dateof.strftime("%m")
    year_of = dateof.strftime("%Y")
    hour_of = timeof.strftime("%H")
    min_of = timeof.strftime("%M")
    sec_of = timeof.strftime("%S")

    start_time = datetime(int(year_of), int(month_of), int(
        date_of), int(hour_of), int(min_of), int(sec_of))
    end_time = start_time + timedelta(minutes=45)
    timezone = 'Asia/Kolkata'

    description = "Appointment with Doctor " + str(doctor)

    event = {
        'summary': 'Doctor Appointment',
        'location': str(city),
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24*60},
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    service.events().insert(calendarId=calendar_id, body=event).execute()


    return end_time

@login_required(login_url='login')
def view_allapp(request):
    data = Appointment.objects.filter(patient_name=request.user)
    return render(request, 'appointment/viewappoint_1.html', {'data': data})