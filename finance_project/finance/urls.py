from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Example route for the homepage
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-income/', views.add_income, name='add_income'),  # Add Income page
    path('add-expense/', views.add_expense, name='add_expense'),  # Add Expense page
]
