from django.shortcuts import render
from userloginp3_app.forms import UserForm, UserInfoForm
from userloginp3_app.models import UserInfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def login_page(request):
	diction = {}
	return render(request,'userloginp3_app/login.html',context=diction)

def user_login(request):
	diction = {}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect(reverse('userloginp3_app:index'))
				# return render(request,'userloginp3_app/index.html',context={})
			else:
				return HttpResponse("Account not activated!")
		else:
			return HttpResponse("Invalid user!")
	else:
		return render(request,'userloginp3_app:login.html',context=diction)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userloginp3_app:index'))

def index(request):
	diction={}
	if request.user.is_authenticated:
		current_user = request.user
		user_id = current_user.id
		user_basic_info = User.objects.get(pk=user_id) # one to one
		user_more_info = UserInfo.objects.get(user__pk=user_id) #seperate 2 column name
		diction = {'user_basic_info':user_basic_info,'user_more_info':user_more_info}

	return render(request,'userloginp3_app/index.html',context=diction)

def register(request):
	
	registered = False # Load for the first time
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		user_info_form = UserInfoForm(data=request.POST)

		if user_form.is_valid() and user_info_form.is_valid():
			user = user_form.save() # username,password,email
			user.set_password(user.password) # encryption password
			user.save() # save all fields

			user_info = user_info_form.save(commit=False) # Wait for validation
			user_info.user = user # connect two forms
			
			# Check whether image is loaded
			if 'profile_pic' in request.FILES:
				user_info.profile_pic = request.FILES['profile_pic']

			user_info.save() # Now commit will be True
			registered = True
	
	else:
		user_form = UserForm()
		user_info_form = UserInfoForm()
	
	diction = {'user_form':user_form,'user_info_form':user_info_form,'registered':registered}
	return render(request,'userloginp3_app/register.html',context=diction)
