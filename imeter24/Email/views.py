from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms
from scom.Email.models import Users
# import time, datetime


class adduserForm(forms.Form):
    name         = forms.CharField(max_length=64)
    password     = forms.CharField(max_length=64)
    email        = forms.EmailField(max_length=64)

class deleteuserForm(forms.Form):
    name         = forms.CharField(max_length=64)



def index(request):
    '''This will be index of users page.'''
    return HttpResponse('This will be an index of mail users.  For now use the Admin interface')

def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = adduserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            vstr = "<p>You entered name (%s), password(%s) and email (%s)</p>" % (form.cleaned_data['name'], form.cleaned_data['password'], form.cleaned_data['email'])
            if Users.objects.filter(source=form.cleaned_data['email']):
                vstr = vstr + '<p> E-mail EXISTS!  You bastard!! </p>'
            else:
                vstr = vstr + '<p> New user email verified... </p>'
            return HttpResponse(vstr)
#            return HttpResponseRedirect('/mail/index') # Redirect after POST
    else:
        form = adduserForm() # An unbound form

    return render_to_response('adduser.html', {
        'form': form,
    })

def delete(request):
    if request.method == 'POST': # If the form has been submitted...
        form = deleteuserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            vstr = "<p>You entered name (%s)</p>" % form.cleaned_data['name']
            if Users.objects.filter(username=form.cleaned_data['name']):
                vstr = vstr + '<p> E-mail EXISTS!  Prepare to be ZAPPED! </p>'
            else:
                vstr = vstr + '<p> Not a valid user! </p>'
            return HttpResponse(vstr)
#            return HttpResponseRedirect('/mail/index') # Redirect after POST
    else:
        form = deleteuserForm() # An unbound form

    return render_to_response('deleteuser.html', {
        'form': form,
    })



