from django.db import models
from django.forms import TextInput


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 8
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {"widget": TextInput(attrs={"type": "color", "list": "appColors"})}
        defaults.update(kwargs)
        return super().formfield(**defaults)
