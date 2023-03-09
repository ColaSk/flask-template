from flask.views import MethodView
from schemas.response_schema import BaseResponseSchema
from utils.response import BaseResponse
from .urls import v1
from schemas.basic_schema import (
    DownloadParserSchema, FileUriSchema, UploadParserSchema, UploadFilesSchema)
from services import basic_service


class PublicUploadView(MethodView):

    @v1.doc(tags=["基础[Basic]"], description="公共上传文件, 不具有保密性", summary="公共上传文件")
    @v1.arguments(UploadParserSchema, location="form")
    @v1.arguments(UploadFilesSchema, location="files")
    @v1.response(200, BaseResponseSchema.set_data(FileUriSchema))
    def post(self, params: dict, files: dict):
        """公共上传文件"""
        data = basic_service.upload_file(files, **params)
        return BaseResponse(data=data)


class DownloadView(MethodView):

    @v1.doc(tags=["基础[Basic]"], description="下载文件", summary="下载文件")
    @v1.arguments(DownloadParserSchema, location="query")
    @v1.response(200, BaseResponseSchema.set_data(FileUriSchema))
    def get(self, params: dict):
        """下载文件"""
        data = basic_service.download_file(**params)
        return BaseResponse(data=data)
