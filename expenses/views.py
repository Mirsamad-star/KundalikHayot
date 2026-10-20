from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Expense, Category

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    type_filter = request.GET.get('type', '')
    if type_filter:
        expenses = expenses.filter(type=type_filter)
    
    # Summary
    total_expense = Expense.objects.filter(user=request.user, type='expense').aggregate(t=Sum('amount'))['t'] or 0
    total_income = Expense.objects.filter(user=request.user, type='income').aggregate(t=Sum('amount'))['t'] or 0
    
    return render(request, 'expenses/list.html', {
        'expenses': expenses,
        'type_filter': type_filter,
        'total_expense': total_expense,
        'total_income': total_income,
        'balance': total_income - total_expense,
    })

@login_required
def expense_create(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        cat_id = request.POST.get('category')
        category = Category.objects.filter(pk=cat_id, user=request.user).first() if cat_id else None
        expense = Expense(
            user=request.user,
            category=category,
            title=request.POST.get('title', ''),
            amount=request.POST.get('amount', 0),
            type=request.POST.get('type', 'expense'),
            date=request.POST.get('date') or timezone.now().date(),
            notes=request.POST.get('notes', ''),
        )
        if 'receipt' in request.FILES:
            expense.receipt = request.FILES['receipt']
        expense.save()
        messages.success(request, 'Recorded successfully!')
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {'action': 'Create', 'categories': categories})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        cat_id = request.POST.get('category')
        expense.category = Category.objects.filter(pk=cat_id, user=request.user).first() if cat_id else None
        expense.title = request.POST.get('title', expense.title)
        expense.amount = request.POST.get('amount', expense.amount)
        expense.type = request.POST.get('type', expense.type)
        expense.date = request.POST.get('date') or expense.date
        expense.notes = request.POST.get('notes', '')
        if 'receipt' in request.FILES:
            expense.receipt = request.FILES['receipt']
        expense.save()
        messages.success(request, 'Updated!')
        return redirect('expense_list')
    return render(request, 'expenses/form.html', {'expense': expense, 'action': 'Edit', 'categories': categories})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Deleted!')
        return redirect('expense_list')
    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

@login_required
def category_manage(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.get_or_create(user=request.user, name=name, defaults={
                'icon': request.POST.get('icon', '💰'),
                'color': request.POST.get('color', '#10b981'),
            })
            messages.success(request, 'Category added!')
        return redirect('category_manage')
    return render(request, 'expenses/categories.html', {'categories': categories})
