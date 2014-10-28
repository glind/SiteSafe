from crispy_forms.helper import FormHelper
from functools import partial
import floppyforms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Reset, HTML, Button, Row, Field
from crispy_forms.bootstrap import  FormActions


from .models import WebSite


class DatePicker(forms.DateInput):
    template_name = 'datepicker.html'

DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class WebSiteForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(WebSiteForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('save', 'save'))

    class Meta:
        model = WebSite


