from marshmallow import fields, Schema
from flask_smorest.fields import Upload


class FileUriSchema(Schema):

    url = fields.URL(required=True)


class DownloadParserSchema(Schema):

    path = fields.Str(required=True)  # 文件路径


class UploadParserSchema(Schema):

    path = fields.Str()


class UploadFilesSchema(Schema):

    files = Upload()
