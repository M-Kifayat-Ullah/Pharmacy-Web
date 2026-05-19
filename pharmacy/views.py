from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Medicine, Invoice, SaleItem
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json

def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    total_medicines = Medicine.objects.count()
    low_stock = Medicine.objects.filter(quantity__lt=10).count()
    total_invoices = Invoice.objects.count()
    return render(request, 'dashboard.html', {
        'total_medicines': total_medicines,
        'low_stock': low_stock,
        'total_invoices': total_invoices
    })

@login_required(login_url='login')
def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

@login_required(login_url='login')
def add_medicine(request):
    if request.method == "POST":
        Medicine.objects.create(
            name=request.POST['name'],
            batch_number=request.POST['batch_number'],
            expiry_date=request.POST['expiry_date'],
            buy_price=request.POST['buy_price'],
            sell_price=request.POST['sell_price'],
            quantity=request.POST['quantity']
        )
        return redirect('medicine_list')
    return render(request, 'add_medicine.html')
@login_required(login_url='login')
def edit_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == "POST":
        medicine.name = request.POST['name']
        medicine.batch_number = request.POST['batch_number']
        medicine.expiry_date = request.POST['expiry_date']
        medicine.buy_price = request.POST['buy_price']
        medicine.sell_price = request.POST['sell_price']
        medicine.quantity = request.POST['quantity']
        medicine.save()
        return redirect('medicine_list')
    return render(request, 'edit_medicine.html', {'medicine': medicine})

@login_required(login_url='login')
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    return redirect('medicine_list')
from django.http import JsonResponse
import json

@login_required(login_url='login')
def billing(request):
    medicines = Medicine.objects.filter(quantity__gt=0)
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'billing.html', {
        'medicines': medicines,
        'invoices': invoices,
        'cashier': request.user.username
    })

@login_required(login_url='login')
def generate_bill(request):
    if request.method == "POST":
        data = json.loads(request.body)
        items = data.get('items', [])
        total = data.get('total', 0)
        
        if not items:
            return JsonResponse({'error': 'No items'}, status=400)
        
        invoice = Invoice.objects.create(
            cashier=request.user.username,
            total_amount=total
        )
        
        for item in items:
            medicine = Medicine.objects.get(id=item['id'])
            SaleItem.objects.create(
                invoice=invoice,
                medicine=medicine,
                quantity=item['quantity'],
                rate=item['price'],
                total=item['total']
            )
            medicine.quantity -= item['quantity']
            medicine.save()
        
        return JsonResponse({'success': True, 'invoice_id': invoice.invoice_number})
    
    return JsonResponse({'error': 'Invalid'}, status=400)

@login_required(login_url='login')
def sales_history(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'sales_history.html', {'invoices': invoices})