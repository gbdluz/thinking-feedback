from django.forms import CheckboxSelectMultiple


class GroupedCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = "custom_widget.html"
