from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from data.models import Plant,Order,OrderItem
from django.conf import settings
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.template.defaultfilters import register
from django.views.decorators.csrf import csrf_exempt
import razorpay
from data.constants import PaymentStatus
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import login, get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

@login_required
def profile(request):
    if request.user.is_authenticated:
        return redirect('display')

def home(request):
    return render(request, 'main.html', {})


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

@login_required
def checkout(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    print(plant)
    return render(request, 'home/checkout.html', {'plant': plant})


@login_required
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
@login_required
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
@login_required
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
@login_required
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

@login_required
def order_payment(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_view')
    
    # Calculate total and create order items
    total = 0
    order_items = []
    
    for pid, qty in cart.items():
        plant = get_object_or_404(Plant, id=pid)
        total += float(plant.price) * qty
        order_items.append({
            'plant': plant,
            'quantity': qty,
            'price': plant.price
        })

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_order = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        # Create order and order items
        order = Order.objects.create(
            user=request.user,
            name=request.user.username,
            amount=total,
            provider_order_id=payment_order["id"]
        )

        # Create order items
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                plant=item['plant'],
                plant_name=item['plant'].name,
                quantity=item['quantity'],
                price=item['price']
            )

        # Update callback URL to use reverse URL resolution
        from django.urls import reverse
        callback_url = request.build_absolute_uri(reverse('payment_callback'))

        payment_data = {
            "callback_url": callback_url,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
        }
        
        return render(request, "payment.html", payment_data)
    
    except Exception as e:
        print(e)
        return render(request, "payment.html", {"error": "Something went wrong"})

@login_required
@csrf_exempt
def callback(request):
    payment_id = request.POST.get("razorpay_payment_id") or request.GET.get("razorpay_payment_id", "")
    order_id = request.POST.get("razorpay_order_id") or request.GET.get("razorpay_order_id", "")
    signature = request.POST.get("razorpay_signature") or request.GET.get("razorpay_signature", "")

    try:
        if not all([payment_id, order_id, signature]):
            return render(request, "callback.html", {
                "status": "failure",
                "message": "Missing payment parameters"
            })

        order = Order.objects.get(provider_order_id=order_id)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        params_dict = {
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
            order.payment_id = payment_id
            order.signature_id = signature
            order.status = PaymentStatus.SUCCESS
            order.save()
            
            # Update inventory and clear cart
            order.update_inventory()
            if 'cart' in request.session:
                del request.session['cart']
                request.session.modified = True
            
            return render(request, "callback.html", {
                "status": "success",
                "message": "Payment successful!",
                "order_id": order.id,
                "amount": order.amount,
                "user": request.user
            })
            
        except Exception as e:
            print(f"Payment verification failed: {e}")
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", {
                "status": "failure",
                "message": "Payment verification failed"
            })
            
    except Order.DoesNotExist:
        return render(request, "callback.html", {
            "status": "failure",
            "message": "Order not found"
        })
    except Exception as e:
        print(f"Callback processing failed: {e}")
        return render(request, "callback.html", {
            "status": "failure",
            "message": "An error occurred during payment processing"
        })