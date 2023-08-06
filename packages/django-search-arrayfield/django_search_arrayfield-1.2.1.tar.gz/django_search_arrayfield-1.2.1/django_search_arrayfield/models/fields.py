from django.contrib.postgres.fields import ArrayField as DjangoArrayField

from ..forms.fields import DynamicArrayField


class ArrayField(DjangoArrayField):
    def formfield(self, **kwargs):
        return super().formfield(**{"form_class": DynamicArrayField, **kwargs})
