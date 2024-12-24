from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'base.html') 

@login_required
def dashboard(request):
    # Fetch user-specific transactions
    income_logs = Income.objects.filter(user=request.user).order_by('-date')
    expense_logs = Expense.objects.filter(user=request.user).order_by('-date')

    # Combine and sort by date
    transactions = sorted(
        list(income_logs) + list(expense_logs),
        key=lambda t: t.date,
        reverse=True
    )

    # Pass categories as dictionaries for JSON conversion
    income_categories = dict(Income.INCOME_CATEGORIES)
    expense_categories = dict(Expense.EXPENSE_CATEGORIES)

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'income_categories': income_categories,
        'expense_categories': expense_categories
    })

@login_required
def add_income(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        Income.objects.create(
            user=request.user,
            category=category,
            description=description,
            amount=amount,
        )
        return redirect('dashboard')

    return render(request, 'add_income.html', {
        'categories': dict(Income.INCOME_CATEGORIES).keys()
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')

        Expense.objects.create(
            user=request.user,
            category=category,
            description=description,
            amount=amount,
        )
        return redirect('dashboard')

    return render(request, 'add_expense.html', {
        'categories': dict(Expense.EXPENSE_CATEGORIES).keys()
    })
