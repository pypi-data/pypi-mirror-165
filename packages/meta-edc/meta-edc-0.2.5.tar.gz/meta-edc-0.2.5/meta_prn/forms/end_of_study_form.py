from django import forms
from edc_action_item.forms import ActionItemFormMixin
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin

from ..form_validators import EndOfStudyFormValidator
from ..models import EndOfStudy


class EndOfStudyForm(
    SiteModelFormMixin,
    ActionItemFormMixin,
    FormValidatorMixin,
    forms.ModelForm,
):

    form_validator_cls = EndOfStudyFormValidator

    subject_identifier = forms.CharField(
        label="Subject Identifier",
        required=False,
        widget=forms.TextInput(attrs={"readonly": "readonly"}),
    )

    class Meta:
        model = EndOfStudy
        fields = "__all__"
        labels = {"offstudy_datetime": "Date patient terminated from study:"}
