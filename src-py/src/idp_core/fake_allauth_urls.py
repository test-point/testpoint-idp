from allauth.account import views as allauth_account_views
from allauth.compat import importlib
from allauth.socialaccount import providers
from django.conf.urls import url


urlpatterns = [
    url(r'^login/$', allauth_account_views.login, name='account_login'),
    url(r'^login/$', allauth_account_views.login, name='account_signup'),
    url(r"^logout/$", allauth_account_views.logout, name="account_logout"),
    url(r"^account/inactive/$", allauth_account_views.account_inactive, name="account_inactive"),
]

for provider in providers.registry.get_list():
    try:
        prov_mod = importlib.import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
