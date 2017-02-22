from django.conf import settings
from django.http import Http404
from django.views.generic import View
from django.shortcuts import redirect


class HomeRedirectView(View):

    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG:
            raise Http404()
        return redirect('http://testpoint.io/idp.html')
