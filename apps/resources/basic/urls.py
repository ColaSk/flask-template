from .. import basic_bp_v1 as v1
from .views import (DownloadView, PublicUploadView)

v1.add_resource(PublicUploadView, '/upload')
v1.add_resource(DownloadView, '/download')
