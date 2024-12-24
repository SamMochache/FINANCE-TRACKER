from django.apps import AppConfig # This is more of a workaround; signals should work without this


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'

       

