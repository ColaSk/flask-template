from .base_schema import RawBaseSchema
from typing import Type, Union

from marshmallow import Schema, fields


class BaseResponseSchema(RawBaseSchema):
    message = fields.String(default="Success", description="Success表示正常", example="Success")
    status = fields.Integer(default=200, description="代表http状态码表示正常", example=200)
    code = fields.Integer(default=200, description="业务码,200代表正常,其他业务码详见message说明", example=200)
    data = fields.Dict(default={})
    request_id = fields.String()

    @classmethod
    def set_data(cls, data_schema: Union[Schema, Type[Schema]]) -> Type:
        lds = type(
            "Response" + data_schema.__class__.__name__,
            (cls, ),
            dict(data=fields.Nested(data_schema), ),
        )
        return lds


class ListDataSchema(RawBaseSchema):
    total = fields.Int()
    items = fields.List(fields.Dict())


class ListResponseSchema(BaseResponseSchema):
    data = fields.Nested(ListDataSchema())

    @classmethod
    def set_item_data(cls, item_schema: Union[Schema, Type[Schema]]) -> Type:
        lds = type(
            "ListData" + item_schema.__class__.__name__,
            (ListDataSchema, ),
            dict(items=fields.List(fields.Nested(item_schema)), ),
        )
        return type(
            "ListResponse" + item_schema.__class__.__name__,
            (ListResponseSchema, ),
            dict(data=fields.Nested(lds)),
        )


class NonPageListResponseSchema(BaseResponseSchema):

    data = fields.List(fields.Dict())

    @classmethod
    def set_data(cls, data_schema: Union[Schema, Type[Schema]]) -> Type:
        lds = type(
            "Response" + data_schema.__class__.__name__,
            (cls, ),
            dict(data=fields.List(fields.Nested(data_schema), ), ),
        )
        return lds
