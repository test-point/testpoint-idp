# from django.contrib.auth import views as auth_views
import oidc_provider
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^allauth/signup/$', RedirectView.as_view(url='/')),
    url(r'^allauth/', include('allauth.urls')),
    url(r'^users/', include('idp_core.users.urls', namespace='users')),
    url(r'^rp/', include('idp_core.rp.urls', namespace='rp')),

    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
    url(r'^logout/?$', oidc_provider.views.EndSessionView.as_view(), name='oidc-logout'),

    url(r'^admin/', include(admin.site.urls)),
]
