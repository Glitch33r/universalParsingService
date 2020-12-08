from django.forms import ModelForm, forms

from main.models import *


class SupportForm(ModelForm):
    class Meta:
        model = SupportMessage
        fields = ['name', 'email', 'text']


class UnitCreateForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['nickname', 'description']

    def clean_nickname(self):
        v = self.cleaned_data['nickname']

        if Unit.objects.filter(nickname=v).exists():
            raise forms.ValidationError('A Unit nickname already exists. It mast be uniq.')

        return v


class UnitFormUpdate(ModelForm):
    disabled_fields = ('nickname', 'user')

    class Meta:
        model = Unit
        fields = ['user', 'nickname', 'description']

    def __init__(self, *args, **kwargs):
        super(UnitFormUpdate, self).__init__(*args, **kwargs)
        for field in self.disabled_fields:
            self.fields[field].disabled = True


class UnitCodeForm(ModelForm):
    class Meta:
        model = UnitCode
        fields = ['code', ]
