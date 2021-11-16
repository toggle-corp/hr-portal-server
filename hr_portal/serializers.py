from rest_framework import serializers


def remove_null(d):
    if not isinstance(d, (dict, list)):
        return d

    if isinstance(d, list):
        return [v for v in (remove_null(v) for v in d) if v is not None]

    return {
        k: v
        for k, v in (
            (k, remove_null(v))
            for k, v in d.items()
        )
        if v is not None
    }


class RemoveNullFieldsMixin():
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return remove_null(rep)

    def to_internal_value(self, data):
        # Change None char fields to blanks
        # TODO: Handle list and dict of charfields as well
        for field, field_type in self.fields.items():
            if isinstance(field_type, serializers.CharField):
                if field in data and not data.get(field):
                    data[field] = ''
        return super().to_internal_value(data)


class WriteOnlyOnCreateSerializerMixin():
    """
    Allow to define fields only writable on creation
    """
    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        write_only_on_create_fields = getattr(self.Meta, 'write_only_on_create_fields', [])
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) != 'POST':
            for field in write_only_on_create_fields:
                fields[field].read_only = True
        return fields
