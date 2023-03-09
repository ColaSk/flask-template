import typing as t
from models import commit


class BaseService(object):

    _model = None

    @commit
    def create(self, request: dict):
        obj = self._model.create(**request)
        return obj

    @commit
    def batch_create(self, request_list: t.List[dict]):
        """批量创建"""
        objs = self._model.bulk_create(request_list)
        return objs

    def list(self, page: int, per_page: int):
        count, objs = self._model.get_by_filter(offset=page, limit=per_page)
        return count, objs

    def get_by_pk(self, pk: int):
        obj = self._model.get_by_id(pk)
        return obj

    @commit
    def delete(self, pk: int):
        obj = self._model.delete(pk)
        return obj

    @commit
    def update(self, pk: int, request: dict):
        obj = self._model.update(pk, **request)
        return obj
