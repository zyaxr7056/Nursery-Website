from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from data.models import Plant
    
@login_required
def profile(request):
    if request.user.is_authenticated:
        return redirect('display')

def home(request):
    return render(request, 'main.html', {})

@login_required
def display(request):
    plants = Plant.objects.all()
    return render(request,'home/display.html', {'plants': plants})

@login_required
def SpecificPlant(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    return render(request, 'home/specific_plant.html', {'plant': plant})

