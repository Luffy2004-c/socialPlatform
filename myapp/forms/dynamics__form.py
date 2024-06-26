from myapp.models import User, Dynamics
from django import forms
from . import ui_form


class DynamicsModelForm(ui_form.CssForm, forms.ModelForm):
    class Meta:
        model = Dynamics
        fields = ["content", "image", "is_public"]
