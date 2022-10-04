from accounts.models import MyUser, Blog, SPECIALITY,Appointment
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import EmailInput, PasswordInput


class RegisterForm(UserCreationForm):
    password1=forms.CharField(label='Password', widget=PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password', widget=PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=MyUser
        fields=['username','email', 'first_name','last_name','password1','password2','address', 'city', 'pincode','state', 'profile_pic','patient', 'doctor']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'passord':forms.PasswordInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'patient':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'doctor':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
            

        }
class LoginForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=['username', 'password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'password1':forms.PasswordInput(attrs={'class':'form-control'})
        }


CATEGORIES = (('Mental Health', 'Mental Health'),
              ('Heart Disease', 'Heart Disease'),
              ('COVID19', 'COVID19'),
              ('Immunization', 'Immunization'))


class BlogCreation(forms.ModelForm):
    title = forms.CharField(
        label='Title of the Blog: ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary = forms.CharField(label='Summary of the Blog: ',
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Content of the Blog: ',
                              widget=forms.Textarea(attrs={'class': 'form-control'}))
    blog_category = forms.ChoiceField(choices=CATEGORIES,
                                      label='Select the Category', widget=forms.Select(attrs={'class': 'form-control'}))
    is_draft = forms.BooleanField(
        label=' Create Draft',
        required=False,
        initial=False)

    class Meta:
        model = Blog
        fields = ['title', 'summary',
                  'content','blog_image' ,'blog_category', 'is_draft']



class AppointmentCreation(forms.ModelForm):
    app_date = forms.DateField(label='Enter the date for the appointment: ',
                               widget=forms.DateInput(attrs={'class': 'form-control'}))
    app_time = forms.TimeField(
        label='Enter the time for the appointment: ', widget=forms.TimeInput(attrs={'class': 'form-control'}))
    speciality = forms.ChoiceField(choices=SPECIALITY,
                                   label='Required Speciality', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Appointment
        fields = ['speciality', 'app_date', 'app_time']