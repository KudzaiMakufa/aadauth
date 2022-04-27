from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required, permission_required
from .forms import PasswordChangeForm
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def home_logout(request):
  logout(request)
  return redirect('/')

def home_login(request):
  if request.method == "POST":

    user = authenticate(username=request.POST.get('username'),password = request.POST.get('password'))
    
    if(user is not None ):
      login(request , user)
        #  create token if doesnt exist
      for user in User.objects.all():
        Token.objects.get_or_create(user=user)
      return redirect('/specimen/dashboard')
    else:
        #    print(request.POST.get('password'))
        messages.add_message(request, messages.ERROR, 'invalid email or password')

  return render(request , "home/signin.html" , {})

def home_profile(request):
  if request.method == "POST":
    # form = PasswordChangeForm(user=request.user, data=request.POST)
    form = PasswordChangeForm(request.POST)
    user = authenticate(username=request.POST.get('username'),password = request.POST.get('password'))
    
    if(form.is_valid()):
      data = form.cleaned_data
      
      user = authenticate(username=request.user.username, password = data['oldpass'])

      if(user is None):
        messages.add_message(request, messages.ERROR, ' Old password is not correct')
        return redirect('/profile')
      elif(data['newpass'] != data['confirmpass']):
        messages.add_message(request, messages.ERROR, ' Passwords did not match')
        return redirect('/profile')
      else:
        u = User.objects.get(username=request.user.username)
        u.set_password(data['newpass'])
        u.save()
        update_session_auth_hash(request, request.user)
        messages.add_message(request, messages.INFO, ' Password changed successfully')
        # return redirect('/profile')
      # return redirect('/specimen/dashboard')
    
  #   if(user is not None ):
  #      login(request , user)
  #      return redirect('/patient/list')
  #   else:
  # #    print(request.POST.get('password'))
  #      messages.add_message(request, messages.ERROR, 'invalid email or password')
  else:
    form = PasswordChangeForm()

  context = {
    'form' : form,
    'title' : 'Profile Information'
  }

  return render(request , "home/profile.html" , context)  



import base64
import binascii

from django.utils.translation import gettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import (
    BasicAuthentication,
    get_authorization_header,
)

from defender import utils
from defender import config

class BasicAuthenticationDefender(BasicAuthentication):

    def get_username_from_request(self, request):
        auth = get_authorization_header(request).split()
        return base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')[0]

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        if utils.is_already_locked(request, get_username=self.get_username_from_request):
            detail = "You have attempted to login {failure_limit} times, with no success." \
                     "Your account is locked for {cooloff_time_seconds} seconds" \
                     "".format(
                        failure_limit=config.FAILURE_LIMIT,
                        cooloff_time_seconds=config.COOLOFF_TIME
                     )
            raise exceptions.AuthenticationFailed(_(detail))

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError, binascii.Error):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        userid, password = auth_parts[0], auth_parts[2]
        login_unsuccessful = False
        login_exception = None
        try:
            response = self.authenticate_credentials(userid, password)
        except exceptions.AuthenticationFailed as e:
            login_unsuccessful = True
            login_exception = e

        utils.add_login_attempt_to_db(request,
                                      login_valid=not login_unsuccessful,
                                      get_username=self.get_username_from_request)
        # add the failed attempt to Redis in case of a failed login or resets the attempt count in case of success
        utils.check_request(request,
                            login_unsuccessful=login_unsuccessful,
                            get_username=self.get_username_from_request)
        if login_unsuccessful:
            raise login_exception

        
        return response