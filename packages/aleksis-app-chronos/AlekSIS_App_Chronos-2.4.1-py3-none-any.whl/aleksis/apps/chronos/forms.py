from django import forms

from django_select2.forms import ModelSelect2MultipleWidget
from material import Layout

from .models import AutomaticPlan, LessonSubstitution


class LessonSubstitutionForm(forms.ModelForm):
    """Form to manage substitutions."""

    class Meta:
        model = LessonSubstitution
        fields = ["subject", "teachers", "room", "cancelled", "comment"]
        widgets = {
            "teachers": ModelSelect2MultipleWidget(
                search_fields=[
                    "first_name__icontains",
                    "last_name__icontains",
                    "short_name__icontains",
                ],
                attrs={"data-minimum-input-length": 0, "class": "browser-default"},
            ),
        }


class AutomaticPlanForm(forms.ModelForm):
    layout = Layout("slug", "name", "number_of_days", "show_header_box")

    class Meta:
        model = AutomaticPlan
        fields = ["slug", "name", "number_of_days", "show_header_box"]
