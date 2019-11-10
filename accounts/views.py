from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
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


def logout(request):
    logout(request)
    return redirect('/')


def forgot_password(request):
    print(request.POST.dict())
    return JsonResponse({"message": "OK"})


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
