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


def return_error_msg(msg, status=400):
    resp = JsonResponse({"success": False, "msg": msg})
    resp.status_code = status
    return resp


def signup(request):
    if request.is_ajax():
        print(request.POST.get('username'))
        if User.objects.filter(username=request.POST.get('username')).exists():
            return return_error_msg('Sorry, but username already exist. Try to change it.')
        else:
            user = User.objects.create(
                first_name=request.POST.get('fullname'),
                username=request.POST.get('username'),
                password=make_password(request.POST.get('password')),
                email=request.POST.get('email'),
                is_active=False,
            )
            message = render_to_string('parts/activate_account_message.html', {
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = request.POST.get('email')
            EmailMessage('Activate Your Account', message, to=[to_email]).send()
            return JsonResponse({"message": "OK"})
    else:
        return return_error_msg('Bad request')


def sign_in(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    elif request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.POST.get('remember') is None:
            request.session.set_expiry(0)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # args['profile'] = user
            return JsonResponse({"message": "OK"})
        else:
            # args['login_error'] = 'User not found!'
            return return_error_msg('Username or/and password are incorrect.')
    else:
        return return_error_msg('Bad request')


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
            user = User.objects.filter(email=u_email)
            if user.exists():
                user = user.first()
                message = render_to_string('parts/reset_password_message.html', {
                    'domain': get_current_site(request),
                    'uid': urlsafe_base64_encode(force_bytes(user.id)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                })
                EmailMessage('Password recovering', message, to=[u_email]).send()
                return JsonResponse({"message": "OK"})
        else:
            return JsonResponse({"message": "OK"})  # little trolling


def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'index.html', {
            'alert_msg': 'Your account has been activate successfully!',
            'alert_type': 'success'
        })
    else:
        return render(request, 'index.html', {
            'alert_msg': 'Activation link is invalid!',
            'alert_type': 'danger'
        })


def password_reset_confirm(request, uidb64, token):
    if request.method == 'GET':
        return render(request, 'parts/change_password.html')
    elif request.is_ajax():
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return render(request, 'index.html', {
                'alert_msg': 'Your password has been updated successfully!',
                'alert_type': 'success'
            })
        else:
            return render(request, 'index.html', {
                'alert_msg': 'Activation link is invalid!',
                'alert_type': 'danger'
            })
    else:
        return render(request, 'index.html', {
            'alert_msg': 'Bad request',
            'alert_type': 'danger'
        })
