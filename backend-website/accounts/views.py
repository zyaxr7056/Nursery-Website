from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from data.models import Plant
from django.conf import settings
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.template.defaultfilters import register


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

@register.filter(name='jsonify')
def jsonify(value):
    return json.dumps(value, cls=DjangoJSONEncoder)

@login_required
def SpecificPlant(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    similar_plants = Plant.objects.filter(Category=plant.Category).exclude(id=plant_id)
    
    # Convert cart data to JSON for JavaScript
    cart = request.session.get('cart', {})
    
    return render(request, 'home/specific_plant.html', {
        'plant': plant,
        'similar_plants': similar_plants,
    })


def checkout(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    print(plant)
    return render(request, 'home/checkout.html', {'plant': plant})



def add_to_cart(request, plant_id):
    cart = request.session.get('cart', {})
    plant_id = str(plant_id)
    
    # Set quantity to 1 if item doesn't exist, otherwise don't change
    if plant_id not in cart:
        cart[plant_id] = 1
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return JsonResponse({
        'cart_count': sum(cart.values()),
        'message': 'Item added to cart successfully'
    })

def update_cart_quantity(request, plant_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        try:
            quantity = int(request.POST.get('quantity', 1))
            plant_id = str(plant_id)
            
            if quantity > 0:
                cart[plant_id] = quantity
            else:
                del cart[plant_id]
                
            request.session['cart'] = cart
            request.session.modified = True
            
            # Recalculate total
            total = 0
            for pid, qty in cart.items():
                plant = get_object_or_404(Plant, id=pid)
                total += plant.price * qty
            
            return JsonResponse({
                'cart_count': sum(cart.values()),
                'total': total
            })
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    
    for pid, qty in cart.items():
        plant = get_object_or_404(Plant, id=pid)
        line_total = plant.price * qty
        items.append({
            'plant': plant,
            'quantity': qty,
            'line_total': line_total,
        })
        total += line_total

    context = {
        'cart_items': items,
        'order': {'total': total},
    }
    
    return render(request, 'home/checkout.html', context)

def remove_from_cart(request, plant_id):
    cart = request.session.get('cart', {})
    plant_id = str(plant_id)
    
    if plant_id in cart:
        del cart[plant_id]
        request.session['cart'] = cart
        request.session.modified = True
        
        # Recalculate total after removal
        total = sum(get_object_or_404(Plant, id=pid).price * qty 
                   for pid, qty in cart.items())
        
        return JsonResponse({
            'cart_count': sum(cart.values()),
            'total': total,
            'message': 'Item removed from cart'
        })
    
    return JsonResponse({
        'error': 'Item not found in cart'
    }, status=404)