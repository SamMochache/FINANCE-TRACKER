# finance/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import F
from .models import Income, Expense, Profile

@receiver(post_delete, sender=Income)
def update_balance_on_income_delete(sender, instance, **kwargs):
    # Subtract the income amount from the balance if the income is deleted
    profile = instance.user.profile
    profile.balance -= instance.amount  # Subtract the income from balance
    profile.save()

@receiver(post_delete, sender=Expense)
def update_balance_on_expense_delete(sender, instance, **kwargs):
    # Add the expense amount back to the balance if the expense is deleted
    profile = instance.user.profile
    profile.balance += instance.amount  # Add the expense amount back to balance
    profile.save()
