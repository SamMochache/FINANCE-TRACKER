from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Example route for the homepage
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),  # Add Income page
    path('add-expense/', views.add_expense, name='add_expense'),  # Add Expense page
    path('create_link_token/', views.create_link_token, name='create_link_token'),
    path('exchange_public_token/', views.exchange_public_token, name='exchange_public_token'),
    path('link_account/', views.link_account, name='link_account'),
]
