from django.urls import path
from .views import *


urlpatterns = [
    path('log-out', logout, name="log-out"),
    path('sign-in', signin, name="sign-in"),
    path('sign-up', signup, name="sign-up"),
    path('forgot-password', forgot_password, name="forgot-password"),
    path('activate/<slug:uidb64>/<slug:token>', activate, name="activate"),
]
