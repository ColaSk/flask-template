from typing import Tuple

from marshmallow import EXCLUDE, Schema, fields, pre_load, post_load
from marshmallow_sqlalchemy import ModelConverter as _ModelConverter
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.convert import _set_meta_kwarg


"""fields args or auto_field kwargs:
default: 序列化默认值
missing: 反序列化默认值
data_key: 外部表示中dict键的名称, load 和 dump 时使用
attribute: 序列化时从中获取值的属性的名称。如果“无”，则假定属性与字段具有相同的名称。
validate: 被调用的验证器或验证器集合在反序列化期间。
    验证器将字段的输入值作为 它的唯一参数，并返回布尔值。
    如果返回“False”, 则会引发: exc:“ValidationError”。
required: 必须传值
allow_none: 如果在期间“none”应被视为有效值，则将其设置为“True”
load_only: 序列化期间跳过
dump_only: 反序列化期间跳过
error_messages: 覆盖默认错误信息
"""


class ModelConverter(_ModelConverter):

    def _get_field_kwargs_for_property(self, prop):
        kwargs = super(ModelConverter, self)._get_field_kwargs_for_property(prop)
        if hasattr(prop, "comment") and 'description' not in kwargs:
            _set_meta_kwarg(kwargs, "description", prop.comment)
        return kwargs


class RawBaseSchema(Schema):

    class Meta:
        strict = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        unknown = EXCLUDE


class BaseSchema(SQLAlchemyAutoSchema):

    class Meta:
        strict = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"
        unknown = EXCLUDE

    create_time = fields.DateTime(dump_only=True)
    update_time = fields.DateTime(dump_only=True)


class PageMixin:
    """Usage

    class SomeSchema(BaseSchema, PageMixin):
        ...

    data = SomeSchema.load(dict(page=0, per_page=10))
    print(data['limit'], data['offset'])
    # TODO: 后续进行替换, 暂时不需要替换
    """

    page = fields.Int(missing=0, validate=lambda x: x >= 0, load_only=True)
    per_page = fields.Int(missing=10, validate=lambda x: x > 0, load_only=True)

    @post_load
    def load_offset_limit(self, data, **kwargs):
        """将page, per_page 转化为 limit, offset"""
        limit, offset = self.page_to_limit(data["page"], data["per_page"])
        data["limit"] = limit
        data["offset"] = offset
        return data

    @staticmethod
    def page_to_limit(page: int, per_page: int) -> Tuple[int, int]:
        """分页转化"""
        limit = per_page
        offset = page * per_page
        return limit, offset


class HeaderSchemaMixin:

    """请求头验证器
    注意事项:
    1. 我们希望仅仅验证头部, 但是又不希望他出现在请求方法的参数里，可以使用 dump_only=True, 但是存在的问题是apidoc将
    不能够捕捉次参数, 因此不采用dump_only参数,但是我们又不想使用它, 可以采用参数 *args捕捉它
    """
    authorization = fields.Str(required=True, data_key='Authorization')


class StrToListMixin:
    """Usage
    class SomeSchema(BaseSchema, StrToListMixin):
        _str_fields = ("some_ids", )

        some_ids = fields.List(fields.Int)


    print(SomeSchema().load({'some_ids': '1,2,3,4'}))
    {
        "some_ids": [1, 2, 3, 4]
    }
    """
    _str_fields: tuple = ()
    _delimiter = ","

    @pre_load
    def str_to_list(self, data, *args, **kwargs):
        """这个方法会将ImmuneMulDict转为MulDict"""
        data = data.copy()
        for field in self._str_fields:
            if field in data:
                value = data[field]
                if isinstance(value, (str, bytes)):
                    try:
                        data[field] = data[field].split(self._delimiter)
                    except Exception as e:
                        print(e)
                        continue
        return data


class HeaderBaseSchema(RawBaseSchema, HeaderSchemaMixin):
    pass
