from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import plaid.configuration
from .models import Income, Expense
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, Profile
from decimal import Decimal, InvalidOperation
from django.http import HttpResponseRedirect
from django.contrib import messages
import plaid
from django.conf import settings
from django.http import JsonResponse
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.configuration import Configuration
from plaid import api_client 


# Create your views here.
def home(request):
    return render(request, 'base.html') 

@login_required
def dashboard(request):
    user = request.user

    # Ensure the profile exists
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    # Fetch user-specific transactions
    income_logs = Income.objects.filter(user=request.user).order_by('-date')
    expense_logs = Expense.objects.filter(user=request.user).order_by('-date')

    # Combine transactions with type information
    transactions = list(income_logs) + list(expense_logs)
    for transaction in transactions:
        if isinstance(transaction, Income):
            transaction.type = 'income'
        elif isinstance(transaction, Expense):
            transaction.type = 'expense'

    # Sort transactions by date
    transactions.sort(key=lambda t: t.date, reverse=True)

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
            messages.error(request, "Please enter a valid amount.")
            return redirect('add_income')


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
        dashboard_url = reverse('dashboard')  # Generates the base URL for the dashboard view
        full_url = f"{dashboard_url}#account-balance-section"

        return HttpResponseRedirect(full_url)
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
            messages.error(request, "Please enter a valid amount.")
            return redirect('add_expense')

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
        dashboard_url = reverse('dashboard')  # Generates the base URL for the dashboard view
        full_url = f"{dashboard_url}#account-balance-section"

        return HttpResponseRedirect(full_url)

    return render(request, 'add_expense.html', {
        'categories': dict(Expense.EXPENSE_CATEGORIES).keys()
    })
# Initialize Plaid API client
client_id = settings.PLAID_CLIENT_ID
secret = settings.PLAID_SECRET
environment = settings.PLAID_ENV  # 'sandbox', 'development', or 'production'
# Map environment string to Plaid environment URL
environment_urls = {
    'sandbox': 'https://sandbox.plaid.com',
    'development': 'https://development.plaid.com',
    'production': 'https://production.plaid.com'
}

# Ensure the environment is valid
if environment not in environment_urls:
    raise ValueError(f"Invalid Plaid environment: {environment}")

# Configure the Plaid client
configuration = Configuration(
    host=environment_urls[environment],
    api_key={
        'clientId': client_id,
        'secret': secret
    }
)

api_client = plaid_api.ApiClient(configuration)
plaid_api_instance = plaid_api.PlaidApi(api_client)

def create_link_token(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be logged in to link a bank account.'}, status=401)
    request_data = LinkTokenCreateRequest(
        client_name="Finance App",
        products=[Products("auth"), Products("transactions")],  # Specify the products
        country_codes=[CountryCode("US")],  # Adjust for the country you're working in
        language='en',
        user=LinkTokenCreateRequestUser(client_user_id=str(request.user.id))
    )

    try:
        # Request a link token from Plaid
        response = plaid_api_instance.link_token_create(request_data)
        return JsonResponse({'link_token': response.link_token})
    except plaid.ApiException as e:
        return JsonResponse({'error': str(e)}, status=500)

def exchange_public_token(request):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User must be logged in to exchange public token.'}, status=401)

    public_token = request.POST.get('public_token')

    if not public_token:
        return JsonResponse({'error': 'public_token is required.'}, status=400)

    # Exchange the public token for an access token
    exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
    try:
        response = plaid_api_instance.item_public_token_exchange(exchange_request)
        access_token = response.access_token
        # You can save the access_token to the database for later use
        return JsonResponse({'access_token': access_token})
    except plaid.ApiException as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def link_account(request):
    return render(request, 'link_account.html')