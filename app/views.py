from django.shortcuts import render
from django.http import HttpResponse
from app.forms import *
from django.core.mail import send_mail
# Create your views here.
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.models import *
def home(request):

    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    

    return render(request,'home.html')


def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()

            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()
            send_mail('Registration',
            'Register Successfull',
            'podduturujeevitha@gmail.com',
            [NSUO.email],
            fail_silently=False)
            
            return HttpResponse('Regsitration is Susssessfulll')
        else:
            return HttpResponse('Not valid')


    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid username or password') 
        
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required   
def Display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    
    return render(request,'Display_profile.html',d)

@login_required
def Change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse("Password IS Updated!!!")
    return render(request,'Change_password.html')

def f_w(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']

        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('Password reset is done')
        else:
            return HttpResponse('username is not avaialble in DB')
    return render(request,'f_w.html')







