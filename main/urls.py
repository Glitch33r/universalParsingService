from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('documentation', faq_page, name='faq'),
    path('add_task', run_bot)
]
