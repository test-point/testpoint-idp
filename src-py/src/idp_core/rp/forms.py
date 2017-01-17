import random
from hashlib import md5
from uuid import uuid4

from django import forms
from oidc_provider.models import Client

from .models import RpInfo

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class RpForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('client_id', 'client_secret')

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-8'
    helper.add_input(Submit('save', 'Add'))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        instance = kwargs.get('instance', None)
        if instance:
            kwargs['instance'] = instance.client
        super(RpForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['client_type'].widget.attrs['class'] = 'form-control'
        self.fields['response_type'].widget.attrs['class'] = 'form-control'
        self.fields['jwt_alg'].widget.attrs['class'] = 'form-control'
        self.fields['_redirect_uris'].widget.attrs['class'] = 'form-control'
        return

    def clean(self):
        instance = getattr(self, 'instance', None)
        client_id = None
        if instance and instance.pk:
            client_id = instance.client_id
        else:
            client_id = str(random.randint(1, 999999)).zfill(6)

        client_secret = ''
        if instance and instance.pk:
            if (self.cleaned_data['client_type'] == 'confidential') and not instance.client_secret:
                client_secret = md5(uuid4().hex.encode()).hexdigest()
            elif (self.cleaned_data['client_type'] == 'confidential') and instance.client_secret:
                client_secret = instance.client_secret
        else:
            if (instance.client_type == 'confidential'):
                client_secret = md5(uuid4().hex.encode()).hexdigest()

        self.cleaned_data['client_id'] = client_id
        self.cleaned_data['client_secret'] = client_secret
        return self.cleaned_data

    def save(self, *args, **kwargs):
        self.instance.client_id = self.cleaned_data.get('client_id')
        self.instance.client_secret = self.cleaned_data.get('client_secret')
        new_client = super(RpForm, self).save(*args, **kwargs)
        try:
            new_client.rpinfo
        except RpInfo.DoesNotExist:
            RpInfo.objects.create(
                user=self.user,
                client=new_client
            )
        return new_client
