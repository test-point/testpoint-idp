import json

from django.contrib.auth import authenticate
from django.conf import settings
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from oidc_provider.lib.utils.token import encode_id_token
from oidc_provider.models import Client as OIDCClient

from idp_core.utils import issue_jwt, get_oidc_client


class HomeRedirectView(View):

    def dispatch(self, request, *args, **kwargs):
        if settings.DEBUG:
            raise Http404()
        return redirect('http://testpoint.io/idp.html')


class ApiTokenCreateView(View):

    def _render(self, data, code=200):
        return HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json',
            status=code
        )

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ApiTokenCreateView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        result = {
            'status': 'success',
        }

        username = request.POST.get('username')
        password = request.POST.get('password')
        client_id = request.POST.get('client_id')

        if not username or not password or not client_id:
            return self._render({
                'status': 'error',
                'details': "Please pass username, password and client_id"
            }, 400)

        user = authenticate(username=username, password=password)
        if user is None:
            return self._render({
                'status': 'error',
                'details': "Wrong username or password"
            }, 400)

        try:
            customer = get_oidc_client(user, client_id)
        except OIDCClient.DoesNotExist:
            return self._render({
                'status': 'error',
                'details': "Given OIDC client (audience) not found"
            }, 400)
        token = issue_jwt(user, customer)
        rendered = encode_id_token(token.id_token, token.client)
        content_rendered = json.dumps(token.id_token)

        result['rendered'] = rendered
        result['content_rendered'] = content_rendered

        return self._render(result)
