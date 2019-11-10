from django.urls import path
from .views import *


urlpatterns = [
    path('log-out', log_out, name="log-out"),
    path('sign-in', signin, name="sign-in"),
    path('sign-up', signup, name="sign-up"),
    path('forgot-password', forgot_password, name="forgot-password"),
    path('password/reset_confirm/<slug:uidb64>/<slug:token>', password_reset_confirm, name="forgot-password"),
    path('activate/<slug:uidb64>/<slug:token>', activate, name="activate"),
]
