from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .models import Payment
import uuid

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # User confirmed they sent the money manually
        
        # Check if a pending payment already exists to avoid duplicates
        Payment.objects.get_or_create(
            order=order,
            defaults={
                'transaction_id': f"MANUAL-{str(uuid.uuid4())[:8]}", # Dummy ID for manual
                'amount': order.get_total_cost(),
                'phone_number': order.phone,
                'status': 'pending'
            }
        )
        
        # Redirect to the pending/waiting page
        return redirect('payment:pending')

    return render(request, 'payment/process.html', {'order': order})

def payment_pending(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('core:home')
        
    order = get_object_or_404(Order, id=order_id)
    
    # Check status logic (Simulating real-time update via page refresh)
    if order.status == 'paid':
        return redirect('payment:done')
    elif order.status == 'canceled':
        return redirect('payment:canceled')
        
    return render(request, 'payment/pending.html', {'order': order})

def payment_done(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        # Verify it is actually paid before showing success (Double check)
        if order.status == 'paid':
             return render(request, 'payment/done.html')
        else:
             return redirect('payment:pending')
             
    return render(request, 'payment/done.html') # Fallback if session missing but accessed directly (rare)

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
