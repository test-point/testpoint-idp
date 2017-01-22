from django.views.generic import View
from django.shortcuts import redirect


class HomeRedirectView(View):

    def dispatch(self, request, *args, **kwargs):
        # future: do something
        return redirect('http://testpoint.io/idp.html')
