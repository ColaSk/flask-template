from marshmallow import ValidationError
from marshmallow.validate import Validator
from models.base import BaseModel
from models.utils import check_object_exist
from utils.exceptions import TipResponse


class ResourceValidator(Validator):
    """资源验证器"""

    def __init__(self, _model: BaseModel, active_only: bool = False) -> None:
        """
        active_only: 如果为true, 保证model下存在active_query属性, 否则设置成为False
        """
        self._model = _model
        self.active_only = active_only

    def __call__(self, value):
        try:
            check_object_exist(self._model, value, self.active_only)
        except TipResponse:
            raise ValidationError(
                f'<{self._model}> This resource <{value}> does not exist')

        return value
