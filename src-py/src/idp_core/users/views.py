import datetime
import json

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DetailView
from oidc_provider.models import Token as OIDCToken, Client as OIDCClient
from oidc_provider.lib.utils.token import create_token, encode_id_token, create_id_token

from .forms import SubUserCreateForm


class MyTokenView(TemplateView):
    template_name = 'users/my_token.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.business.is_synthetic:
            messages.warning(request, 'This page is available only for synthetic users')
            return redirect('/')
        return super(MyTokenView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        c = super(MyTokenView, self).get_context_data(*args, **kwargs)
        tokens = OIDCToken.objects.filter(
            user=self.request.user
        ).order_by('-id')[:15]
        for token in tokens:
            token.rendered = encode_id_token(token.id_token, token.client)
            token.content_rendered = json.dumps(token.id_token)
        c['tokens'] = tokens
        c['clients'] = self.get_clients()
        return c

    def post(self, request, *args, **kwargs):
        customer = self.get_clients().get(client_id=request.POST.get('client'))
        recent_token = create_token(
            user=request.user,
            client=customer,
            scope=["openid"]
        )
        id_token_dic = create_id_token(
            user=request.user,
            aud=customer.client_id,
            nonce=None,
            at_hash=recent_token.at_hash,
            request=None,
            scope=recent_token.scope,
        )
        id_token_dic.update(request.user.business.get_extra_data())
        recent_token.id_token = id_token_dic
        recent_token.expires_at = datetime.datetime.fromtimestamp(
            id_token_dic.get('exp')
        )
        recent_token.save()
        return redirect(request.path_info)

    def get_clients(self):
        # get clients, global and user-specific only, without private clients for another users
        return OIDCClient.objects.filter(
            rpinfo__isnull=True
        ) | OIDCClient.objects.filter(
            rpinfo__user=self.request.user.business.parent_user
        )


class DeveloperRequiredMixin(object):
    """
    Ensure view available only to legal authenticated and validated users (like
    github ones), not to synthetic users created by them.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated() or not request.user.business.is_developer:
            messages.warning(request, 'Please authenticate as developer to access this page')
            return redirect('/')
        return super(DeveloperRequiredMixin, self).dispatch(request, *args, **kwargs)


class UsersListView(DeveloperRequiredMixin, TemplateView):
    template_name = 'users/list.html'


class UserCreateView(DeveloperRequiredMixin, CreateView):
    template_name = 'users/create.html'
    form_class = SubUserCreateForm

    def get_form_kwargs(self):
        kwargs = super(UserCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'User created; password set.')
        return reverse('users:list')


class UserDetailView(DeveloperRequiredMixin, DetailView):
    template_name = 'users/detail.html'

    def get_object(self):
        username = self.kwargs['username']
        try:
            username = int(username)
        except (ValueError, TypeError):
            raise Http404()
        user_model = get_user_model()
        try:
            user = user_model.objects.get(
                username=username
            )
        except user_model.DoesNotExist:
            raise Http404()
        if not user.business.parent_user == self.request.user:
            raise Http404()
        return user

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if 'save' in request.POST:
            new_password = request.POST.get('password', '').strip()
            if new_password:
                obj.set_password(new_password)
                obj.save()
                messages.success(request, 'Password updated')
        elif 'delete' in request.POST:
            obj.delete()
            messages.success(request, 'User deleted')
            return redirect('users:list')
        return redirect(request.path_info)
