from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from app.forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def registration(request):
    ufo=userForm()
    pfo=profileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=userForm(request.POST)
        pfd=profileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            UFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            UFDO.set_password(pw)
            UFDO.save()
            PFDO=pfd.save(commit=False)
            PFDO.username=UFDO
            PFDO.save()
            send_mail('registration',
                      'Dear user your Registrstion is scuccessfull',
                      'akhilreddykond01@gmail.com',
                      [UFDO.email],
                      fail_silently=False,
                      )
            
            return HttpResponse('Registration Is DONE')
        else:
            return HttpResponse('Invalid data')
        



    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')





def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'display_profile.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        uo=User.objects.get(username=username)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('password is Changed Successfully')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Reset is Done')
        else:
            return HttpResponse('Your Username is Not Our Database')
        
    return render(request,'reset_password.html') 




