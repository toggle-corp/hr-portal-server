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


class IntegerIDField(serializers.IntegerField):
    """
    This field is created to override the graphene conversion of the integerfield
    """
    pass


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


class MetaInformationSerializerMixin(serializers.Serializer):
    """
    Responsible to add following fields into the validated data
    - created_by
    - last_modified_by
    """
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    modified_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs) -> dict:
        attrs = super().validate(attrs)
        if self.instance is None:
            attrs.update({
                'created_by': self.context['request'].user
            })
        else:
            attrs.update({
                'modified_by': self.context['request'].user
            })
        return attrs


class UpdateSerializerMixin:
    """Makes all fields not required apart from the id field"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # all updates will be a patch update
        for name in self.fields:
            self.fields[name].required = False
        self.fields['id'].required = True
