from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .token_generator import account_activation_token


def signup(request):
    if request.is_ajax():
        user = User.objects.create(
            first_name=request.POST.get('fullname'),
            password=make_password(request.POST.get('password')),
            email=request.POST.get('email'),
            is_active=False,
        )
        # print(urlsafe_base64_encode(force_bytes(user.id)))
        current_site = get_current_site(request)
        email_subject = 'Activate Your Account'
        message = render_to_string('parts/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.POST.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return JsonResponse({"message": "OK"})
    else:
        return JsonResponse({"success": False, "error": "there was an error"})


def signin(request):
    if request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # args['profile'] = user
            return JsonResponse({"message": "OK"})
        else:
            # args['login_error'] = 'User not found!'
            return JsonResponse({"success": False, "error": "there was an error"})
    else:
        return JsonResponse({"success": False, "error": "there was an error"})


def log_out(request):
    logout(request)
    return redirect('/')


def email_validation(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def forgot_password(request):
    if request.is_ajax():
        u_email = request.POST.get('email')

        if email_validation(u_email):
            user = User.objects.filter(email=u_email).first()
            if user.exists():
                current_site = get_current_site(request)
                message = render_to_string('', {
                    'email': user.email,
                    'domain': current_site,
                    'site_name': 'your site',
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                })
                subject_template_name = 'registration/password_reset_subject.txt'

                email_template_name = 'registration/password_reset_email.html'

                subject = 'Password recovering'

                email = EmailMessage(subject, message, to=[u_email])
                email.send()
                return JsonResponse({"message": "OK"})
        else:
            return JsonResponse({"success": False, "error": "there was an error"})


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.is_ajax():
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return HttpResponse('Your password has been upadated successfully')
        else:
            return HttpResponse('BAD request')
    else:
        return HttpResponse('Activation link is invalid!')
