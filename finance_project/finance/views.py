from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, Profile
from decimal import Decimal, InvalidOperation
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'base.html') 

@login_required
def dashboard(request):
    user = request.user
    # Ensure the profile exists, if not create one
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    # Fetch user-specific transactions
    income_logs = Income.objects.filter(user=request.user).order_by('-date')
    expense_logs = Expense.objects.filter(user=request.user).order_by('-date')

    # Combine and sort by date
    transactions = sorted(
        list(income_logs) + list(expense_logs),
        key=lambda t: t.date,
        reverse=True
    )
    # Fetch user balance
    balance = request.user.profile.balance

    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'balance': balance,
    })

@login_required
def add_income(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        try:
            # Convert the amount to Decimal to avoid type issues
            amount = Decimal(amount)
        except (ValueError, InvalidOperation):
            return HttpResponse("Invalid amount entered", status=400)


        Income.objects.create(
            user=request.user,
            category=category,
            description=description,
            amount=amount,
        )
        # Update user balance
        profile = request.user.profile
        profile.balance += amount
        profile.save()
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

        try:
            # Convert the amount to Decimal to avoid type issues
            amount = Decimal(amount)
        except (ValueError, InvalidOperation):
            return HttpResponse("Invalid amount entered", status=400)

        Expense.objects.create(
            user=request.user,
            category=category,
            description=description,
            amount=amount,
        )
        # Update user balance
        profile = request.user.profile
        profile.balance -= amount
        profile.save()
        return redirect('dashboard')

    return render(request, 'add_expense.html', {
        'categories': dict(Expense.EXPENSE_CATEGORIES).keys()
    })
