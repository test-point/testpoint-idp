# from django.contrib.auth import views as auth_views
import oidc_provider
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

from .views import HomeRedirectView

urlpatterns = [
    url(r'^$', HomeRedirectView.as_view(), name='home'),
    url(r'^allauth/signup/$', RedirectView.as_view(url='/')),
    url(r'^login/$', RedirectView.as_view(url='/allauth/login/')),
    url(r'^allauth/', include('allauth.urls')),
    url(r'^users/', include('idp_core.users.urls', namespace='users')),
    url(r'^rp/', include('idp_core.rp.urls', namespace='rp')),

    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
    url(r'^logout/?$', oidc_provider.views.EndSessionView.as_view(), name='oidc-logout'),

    url(r'^admin/', include(admin.site.urls)),
]
