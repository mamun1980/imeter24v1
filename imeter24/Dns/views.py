from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django import forms

from django.template.defaulttags import csrf_token
from django.shortcuts import render


#@csrf_token
#def newdomaintoken(request):
#    return render(request,
#        'newdomain.html',
#            {}
#    )




from scom.Dns.models import DNS_Data, zonesorted
import time

class newdomainForm(forms.Form):
    zone       = forms.CharField(max_length=64)
    accountid  = forms.CharField(max_length=10)

def enter(request):
    if request.method == 'POST': # If the form has been submitted...
        form = newdomainForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            if DNS_Data.objects.filter(zone=form.cleaned_data['zone']):
                errordata = {
                    'zone': form.cleaned_data['zone'],
                    'accountid': form.cleaned_data['accountid'],
                    }
                form = newdomainForm(errordata)
                return render_to_response('newdomain.html', {'form': form, 'error_message': 'Zone Already Exists!', })
            else:
                # return HttpResponse(reverse('createview')+'?zone='+ form.cleaned_data['zone']+'&accountid='+ form.cleaned_data['accountid'])
                return HttpResponseRedirect(reverse('createview')+'?zone='+ form.cleaned_data['zone']+'&accountid='+ form.cleaned_data['accountid']) # Redirect after POST
    else:
        form = newdomainForm() # An unbound form
    return render_to_response('newdomain.html', {'form': form, })


def index(request):
    '''This will be index page.'''
    DNSrecords = zonesorted.objects.all()
    return render_to_response('info.html', {'DNSrecords': DNSrecords})


def create(request):
    '''This will be create domain page.'''
    targetzone = request.GET['zone'].lower()
    useraccount = request.GET['accountid']
    
    if DNS_Data.objects.filter(zone=targetzone):
        raise Http404

    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, primary_ns=targetzone+".", host="@", type="SOA", data=targetzone+".", resp_person="nobody", serial=int(time.time()), refresh=43200, retry=3600, expire=86400, minimum=3600, ttl=3600)
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="NS", data="ns1.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="NS", data="ns2.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="TXT", host="@", data="v=spf1 ip4:216.106.96.0/24 a mx a:ns1.scom.ca a:ns2.scom.ca a:mail.scom.ca mx:mail.scom.ca -all", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="@", data="216.106.96.16", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="www", data="216.106.96.16", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="webmail", data="216.106.96.22", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="webmail", data="216.106.96.23", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="tmda", data="216.106.96.8", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="A", host="tmda", data="216.106.96.10", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="CNAME", host="mail", data="mail.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="CNAME", host="smtp", data="mail.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="CNAME", host="pop3", data="mail.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="CNAME", host="imap", data="mail.scom.ca.", primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="MX", host="@", data="mail10.scom.ca.", mx_priority=10, primary_ns=" ", resp_person=" ")
    DNS_Data.objects.create(zone=targetzone, accountid=useraccount, type="MX", host="@", data="mail11.scom.ca.", mx_priority=10, primary_ns=" ", resp_person=" ")
    
    return HttpResponseRedirect(reverse('infoview')+'?zone='+targetzone)
    
def info(request):
    '''This will display all domain records'''
    targetzone = request.GET['zone']
    try:
        DNSrecords = DNS_Data.objects.filter(zone=targetzone).order_by('id')
    except DNS_Data.DoesNotExist:
        raise Http404
    return render_to_response('info.html', {'DNSrecords': DNSrecords})


#EOF
