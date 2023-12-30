import copy
from typing import Any, Mapping
from marshmallow import Schema, post_load, fields
from marshmallow.fields import Field
from marshmallow.utils import missing as missing_, resolve_field_instance, FieldInstanceResolutionError

from music_sync.core.download import MetadataActions
from music_sync.core.utils import get_absolute_path


class FieldWrapper(fields.Field):

    def __init__(self, cls_or_instance: fields.Field | type, **kwargs) -> None:
        super().__init__(**kwargs)
        try:
            self.inner = resolve_field_instance(cls_or_instance)
        except FieldInstanceResolutionError as error:
            raise ValueError(
                "The list elements must be a subclass or instance of "
                "marshmallow.base.FieldABC."
            ) from error

    def _bind_to_schema(self, field_name, parent):
        super()._bind_to_schema(field_name, parent)
        self.inner = copy.deepcopy(self.inner)
        self.inner._bind_to_schema(field_name, self)

    def _deserialize(self, value, *args, **kwargs):
        return self.inner._deserialize(value, *args, **kwargs)

    def _serialize(self, *args, **kwargs):
        return self.inner._serialize(*args, **kwargs)


class ContextAware(FieldWrapper):

    def __init__(self,
                 cls_or_instance: Field | type,
                 context_key: str | None = None,
                 context_read_key: str | None = None,
                 context_write_key: str | None = None,
                 **kwargs) -> None:
        super().__init__(cls_or_instance, **kwargs)
        self.context_read_key = context_read_key or context_key
        self.context_write_key = context_write_key or context_key

    def get_value_from_context(self, default_key):
        context_key = default_key if self.context_read_key is None else self.context_read_key

        if context_key not in self.context:
            if self.inner.required:
                raise self.make_error("required")
            else:
                return missing_
        return self.context[context_key]

    def set_value_in_context(self, default_key, value):
        context_key = default_key if self.context_write_key is None else self.context_write_key
        self.context[context_key] = value

    def deserialize(self, value: Any, attr: str | None = None, data: Mapping[str, Any] | None = None, **kwargs):
        if value == missing_:
            value = self.get_value_from_context(attr)

        return super().deserialize(value, attr, data, **kwargs)

    def _deserialize(self, value, attr, data, *args, **kwargs):
        value = super()._deserialize(value, attr, data, *args, **kwargs)
        self.set_value_in_context(attr, value)
        return value


class GetContext(fields.Field):

    def __init__(self,
                 context_key: str | None = None,
                 context_read_key: str | None = None,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.context_read_key = context_read_key or context_key

    def get_value_from_context(self, default_key):
        context_key = default_key if self.context_read_key is None else self.context_read_key

        if context_key not in self.context:
            if self.required:
                raise self.make_error("required")
            else:
                return missing_
        return self.context[context_key]

    def deserialize(self, value: Any, attr: str | None = None, data: Mapping[str, Any] | None = None, **kwargs):
        return self.get_value_from_context(attr)


class PathField(fields.String):

    def __init__(self, base_path='base_path', **kwargs):
        super().__init__(**kwargs)
        self.base_path = base_path

    def _deserialize(self, value, attr, data, **kwargs) -> str:
        string = super()._deserialize(value, attr, data, **kwargs)
        if self.base_path in self.context:
            return get_absolute_path(string, base_path=self.context[self.base_path])
        return get_absolute_path(string)


class MetadataActionsSchema(Schema):
    interpret = fields.List(fields.String(), dump_default=['"SoundCloud Likes" (?s)(?P<album>.+)',
                            '"Various Artists" (?s)(?P<album_artist>.+)',
                                                           '"" (?P<description>)'])
    replace = fields.List(fields.String(), dump_default=[
        'artist,uploader approachingnirvana "Approaching Nirvana"'])

    @post_load
    def to_MetadataAction(self, data, **kwargs):
        actions = MetadataActions()
        if 'interpret' in data:
            actions.parse(data['interpret'], 'interpret')
        if 'replace' in data:
            actions.parse(data['replace'], 'replace')
        return actions
