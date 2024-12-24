from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    INCOME_CATEGORIES = [
        ('salary', 'Salary'),
        ('business', 'Business'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    category = models.CharField(max_length=50, choices=INCOME_CATEGORIES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Income - {self.category.capitalize()}: {self.amount}"

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('groceries', 'Groceries'),
        ('entertainment', 'Entertainment'),
        ('utilities', 'Utilities'),
        ('health', 'Health'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense - {self.category.capitalize()}: {self.amount}"
