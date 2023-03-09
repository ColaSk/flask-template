import os
from werkzeug.utils import secure_filename
from configs.sysconf import API_SERVER, STATIC_FOLDER, STATIC_URL_PATH
from utils.datetime_tools import get_current_timestamp
from utils.exceptions import TipResponse


class BasicService(object):

    def download_file(self, path: str):
        """下载文件,获取文件url
        """

        filepath = os.path.join(STATIC_FOLDER, path)

        if not os.path.exists(filepath):
            raise TipResponse("此文件不存在")

        return {
            "url": f'{API_SERVER}{STATIC_URL_PATH}/{path}'
        }

    def upload_file(self, files: dict, path: str = None):
        """上传文件"""

        def create_filename(type: str):
            return str(get_current_timestamp(by_ms=True)) + '.' + type

        filepath = STATIC_FOLDER
        urlpath = STATIC_URL_PATH
        if path:
            filepath = os.path.join(STATIC_FOLDER, path)
            urlpath = os.path.join(STATIC_URL_PATH, path)

        os.makedirs(filepath, exist_ok=True)

        file = files['files']

        filename = secure_filename(file.filename)
        filetype = filename.split('.')[-1]

        newfilename = create_filename(filetype)
        filepath = os.path.join(filepath, newfilename)
        file.save(filepath)

        return {
            "url": f'{API_SERVER}{urlpath}/{newfilename}'
        }


basic_service = BasicService()
