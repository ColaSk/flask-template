from .base import BaseModel
from utils.exceptions import TipResponse


def check_object_exist(model: BaseModel, _id: int, active_only: bool = True):
    """检查资源是否存在
    """
    instance = model.get_by_id(_id, active_only)
    if not instance:
        raise TipResponse(
            f"此实体 {model} 不存在 <_id: {_id} - active_only: {active_only}>")
    return instance
