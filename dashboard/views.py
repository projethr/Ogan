from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from orders.models import Order
from store.models import Product, Category
from django.db.models import Sum

def staff_required(user):
    return user.is_staff

def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('dashboard:index')
            else:
                # Add error message logic here if needed, or form will handle it generically
                pass
    else:
        form = AuthenticationForm()
    
    return render(request, 'dashboard/login.html', {'form': form})

@user_passes_test(staff_required, login_url='dashboard:login')
def index(request):
    # Stats logic will go here
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    # Handle None if no orders
    revenue_data = Order.objects.filter(is_paid=True).aggregate(Sum('items__price'))
    # Note: Aggregate sum might need more complex logic if items__price is unit price * quantity.
    # Actually Order.get_total_cost is a method, not a field. 
    # For optimized query we might need to annotate or iterate.
    # For MVP let's iterate or use a simple sum if possible. 
    # Better: Calculate properly using Python for now to be safe with methods.
    
    paid_orders = Order.objects.filter(is_paid=True)
    total_revenue = sum(order.get_total_cost() for order in paid_orders)
    
    context = {
        'orders_count': orders_count,
        'products_count': products_count,
        'total_revenue': total_revenue,
        'recent_orders': Order.objects.all().order_by('-created_at')[:5]
    }
    return render(request, 'dashboard/index.html', context)

# --- PRODUCTS ---
from .forms import ProductForm
from django.shortcuts import get_object_or_404

@user_passes_test(staff_required, login_url='dashboard:login')
def product_list(request):
    products = Product.objects.all().select_related('category').order_by('-created_at')
    return render(request, 'dashboard/products/list.html', {'products': products})

@user_passes_test(staff_required, login_url='dashboard:login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': 'Ajouter un produit'})

@user_passes_test(staff_required, login_url='dashboard:login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': f'Modifier {product.name}'})

@user_passes_test(staff_required, login_url='dashboard:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:product_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': product, 'cancel_url': 'dashboard:product_list'})


@user_passes_test(staff_required, login_url='dashboard:login')
def order_list(request):
    status = request.GET.get('status')
    orders = Order.objects.all().order_by('-created_at')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'dashboard/orders/list.html', {'orders': orders})

@user_passes_test(staff_required, login_url='dashboard:login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'dashboard/orders/detail.html', {'order': order})

@user_passes_test(staff_required, login_url='dashboard:login')
def order_mark_paid(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'paid'
        order.is_paid = True
        order.save()
        # Stock management could be here if not already handled elsewhere
    return redirect('dashboard:order_detail', pk=pk)

@user_passes_test(staff_required, login_url='dashboard:login')
def order_mark_delivered(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'delivered'
        order.save()
    return redirect('dashboard:order_detail', pk=pk)

@user_passes_test(staff_required, login_url='dashboard:login')
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = 'cancelled' # Check spelling usage in models (cancelled vs canceled)
        order.save()
        # Restore stock logic would go here
    return redirect('dashboard:order_detail', pk=pk)

# --- CATEGORIES ---
from .forms import CategoryForm

@user_passes_test(staff_required, login_url='dashboard:login')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories/list.html', {'categories': categories})

@user_passes_test(staff_required, login_url='dashboard:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': 'Ajouter une catégorie'})

@user_passes_test(staff_required, login_url='dashboard:login')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': f'Modifier {category.name}'})

@user_passes_test(staff_required, login_url='dashboard:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/confirm_delete.html', {'object': category, 'cancel_url': 'dashboard:category_list'})

