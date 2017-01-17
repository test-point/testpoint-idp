from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class SubUserCreateForm(forms.Form):
    abn = forms.IntegerField(label='ABN')
    password = forms.CharField(widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-8'
    helper.layout = Layout(
        'abn', 'password',
        FormActions(
            Submit('save', 'Add')
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance')
        super(SubUserCreateForm, self).__init__(*args, **kwargs)
        return

    def clean_abn(self):
        value = self.cleaned_data.get('abn')
        busy_users = get_user_model().objects.filter(
            username=value
        ).exists()
        if busy_users:
            raise forms.ValidationError('Sorry, this ABN already busy')
        return value

    def clean_password(self):
        value = self.cleaned_data.get('password')
        if not value:
            raise forms.ValidationError('Please enter non-empty password')
        return value

    def save(self, *args, **kwargs):
        new_user = get_user_model().objects.create(
            username=self.cleaned_data.get('abn'),
            email=self.user.email
        )
        new_user.set_password(self.cleaned_data.get("password"))
        new_user.save()
        new_user.business.parent_user = self.user
        new_user.business.set_extra_data({'abn': new_user.username})
        new_user.business.save()
        return new_user
