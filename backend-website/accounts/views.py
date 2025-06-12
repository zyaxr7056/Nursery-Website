from django.shortcuts import render
from django.contrib.auth.decorators import login_required

    
@login_required
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'user':request.user})
    else:
        return render(request,'login.html',{})

def home(request):
    return render(request, 'main.html', {})