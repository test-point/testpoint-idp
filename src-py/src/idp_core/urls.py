import oidc_provider
from allauth.account import views as allauth_account_views
from django.conf.urls import include, url
from django.contrib import admin

from .views import HomeRedirectView, ApiTokenCreateView

urlpatterns = [
    url(r'^$', HomeRedirectView.as_view(), name='home'),
    url(r'^api/token/create/$', ApiTokenCreateView.as_view(), name='api-get-token'),

    url(r'^login/$', allauth_account_views.login, name='account_login'),
    url(r'^allauth/', include('idp_core.fake_allauth_urls')),

    url(r'^users/', include('idp_core.users.urls', namespace='users')),
    url(r'^rp/', include('idp_core.rp.urls', namespace='rp')),

    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
    url(r'^logout/?$', oidc_provider.views.EndSessionView.as_view(), name='oidc-logout'),

    url(r'^admin/', include(admin.site.urls)),
]
