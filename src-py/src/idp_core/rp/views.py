from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, UpdateView

from idp_core.users.views import DeveloperRequiredMixin
from .forms import RpForm
from .models import RpInfo


class RPListView(DeveloperRequiredMixin, TemplateView):
    template_name = 'rp/list.html'


class RPCreateView(DeveloperRequiredMixin, CreateView):
    template_name = 'rp/create.html'
    form_class = RpForm

    def get_form_kwargs(self):
        kwargs = super(RPCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'RP created')
        return reverse('rp:list')


class RPDetailView(DeveloperRequiredMixin, UpdateView):
    template_name = 'rp/detail.html'
    form_class = RpForm

    def get_object(self):
        rp_id = self.kwargs['id']
        try:
            rp_id = int(rp_id)
        except (ValueError, TypeError):
            raise Http404()

        try:
            rp = RpInfo.objects.get(
                user=self.request.user,
                id=rp_id
            )
        except RpInfo.DoesNotExist:
            raise Http404()
        return rp

    def get_form_kwargs(self):
        kwargs = super(RPDetailView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Relaying Party saved')
        return reverse('rp:detail', args=[self.object.rpinfo.id])

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            obj = self.get_object()
            obj.client.delete()
            messages.success(self.request, 'Relaying Party deleted')
            return redirect('rp:list')
        return super(RPDetailView, self).post(request, *args, **kwargs)
