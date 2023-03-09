from datetime import datetime

from sqlalchemy import DateTime, Integer, Text, Boolean, JSON
from sqlalchemy import Column

from initialization.sqlalchemy_process import db, session


class ActiveQuery:

    def __set__(self, instance):
        return

    def __get__(self, instance, owner):
        return owner.query.filter_by(is_deleted=False)


class BaseEntity(db.Model):
    """基础实体"""

    __abstract__ = True

    def auto_set_attr(self, **data):
        session.refresh(self)
        for k, v in data.items():
            if hasattr(self, k) and k != "id":
                setattr(self, k, v)


class PkBaseEntity(BaseEntity):
    """主键抽象基础实体"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")


class TimeBaseEntity(BaseEntity):
    """时间抽象基础实体"""

    __abstract__ = True

    create_time = Column(DateTime, default=datetime.now, comment="修改时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="最近修改时间")


class IsDelBaseEntity(BaseEntity):

    __abstract__ = True

    is_deleted = Column(Boolean, default=False, comment="是否删除")

    active_query = ActiveQuery()


class DescBaseEntity(BaseEntity):
    """备注描述"""

    __abstract__ = True

    description = Column(Text, comment="备注描述")


class ExtraBaseEntity(BaseEntity):

    __abstract__ = True

    extra_info = Column(JSON, comment="扩展信息")
