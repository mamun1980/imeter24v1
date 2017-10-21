from django.contrib.admin import AdminSite
from django.http import HttpResponse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import views as auth_views
from django.urls import NoReverseMatch, reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.utils.translation import ugettext as _, ugettext_lazy
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

from imeter24.Devices.models import *
from .views import *



class MeterReadSite(AdminSite):

    def login(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        # import pdb; pdb.set_trace();
        if request.method == 'GET' and self.has_permission(request):
            # Already logged-in, redirect to admin index
            index_path = reverse('user:index', current_app=self.name)
            return HttpResponseRedirect(index_path)
        # elif request.method == 'POST':
        #     form = AuthenticationForm(data=request.POST)


        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.admin.forms eventually imports User.
        from django.contrib.admin.forms import AdminAuthenticationForm
        context = dict(
            self.each_context(request),
            title=_('Log in'),
            app_path=request.get_full_path(),
            username=request.user.get_username(),
        )
        if (REDIRECT_FIELD_NAME not in request.GET and
                REDIRECT_FIELD_NAME not in request.POST):
            context[REDIRECT_FIELD_NAME] = reverse('user:index', current_app=self.name)
        context.update(extra_context or {})

        defaults = {
            'extra_context': context,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'user/login.html',
        }
        request.current_app = self.name
        return auth_views.login(request, **defaults)


    def index(self, request, extra_context=None):

        if request.user.username == 'admin' or request.user.is_superuser == True:
            return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/user/dashboard")


    def get_urls(self):
        from django.conf.urls import url


        urls = super(MeterReadSite, self).get_urls()
        urls += [
            url(r'^dashboard/$', self.admin_view(dashboard)),
            url(r'^customers.json$', self.admin_view(customer_list_json)),
            url(r'^(?P<soldto>[0-9]+)/contacts/$', device_data_for_soldto),
            url(r'^(?P<soldto>[^/]+)/(?P<locid>[^/]+)/(?P<regid>[^/]+)/locations/$', locations),
            url(r'^(?P<soldto>[\w]+)/(?P<locid>[^/]+)/(?P<id>[^/]+)/meters/$', meters),

            # url(r'^devices/$', self.admin_view(devices))
        ]
        # urls += super(ImeterAdminSite, self).get_urls()

        return urls
