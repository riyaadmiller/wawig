from django import forms
from crispy_forms.helper                             import FormHelper
from crispy_forms.layout                             import Layout, Row, Column


class WaWiGForm(forms.Form):

    DAYS_CHOICES = [tuple([x, x]) for x in range(1, 6)]

    city = forms.CharField(label="Enter the city's name", max_length=25)
    days = forms.ChoiceField(choices=DAYS_CHOICES, label="Select forecast period in days [max 5]")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                Column('city', css_class='form-group'),
            ),
            Row(
                Column('days', css_class='form-group'),
            )
        )
