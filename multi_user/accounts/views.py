from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm, RegisterForm, BlogCreation
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.models import MyUser, Blog
from unicodedata import category
from django.db.models import Q

from django.shortcuts import render

# Create your views here.



def register_page(request):
	forms=RegisterForm()
	if request.method=='POST':
		form=RegisterForm(request.POST)
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