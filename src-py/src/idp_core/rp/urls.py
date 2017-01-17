from django.conf.urls import url

from .views import RPListView, RPCreateView, RPDetailView

urlpatterns = [
    url(r'^$', RPListView.as_view(), name='list'),
    url(r'^create/$', RPCreateView.as_view(), name='create'),
    url(r'^(?P<id>\d+)/$', RPDetailView.as_view(), name='detail'),
]
