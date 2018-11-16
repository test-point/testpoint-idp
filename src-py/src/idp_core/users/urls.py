from django.conf.urls import url

from .views import UsersListView, UserCreateView, UserDetailView, MyTokenView

urlpatterns = [
    url(r'^$', UsersListView.as_view(), name='list'),
    url(r'^create/$', UserCreateView.as_view(), name='create'),
    url(r'^(?P<username>.+)/$', UserDetailView.as_view(), name='detail'),
    url(r'^my_token/$', MyTokenView.as_view(), name='my_token'),
]
