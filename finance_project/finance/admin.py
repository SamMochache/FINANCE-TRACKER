from django.contrib import admin
from .models import Income, Expense
# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'amount', 'date')  # Fields to display in admin
    list_filter = ('category', 'date')  # Filters for admin sidebar
    search_fields = ('description', 'category')  # Search bar fields

# Custom admin for Expense
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'description', 'amount', 'date')  # Fields to display in admin
    list_filter = ('category', 'date')  # Filters for admin sidebar
    search_fields = ('description', 'category')  # Search bar fields

# Register models with custom admin
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
