from pydantic import (
    BaseConfig as PydanticBaseConfig,
    BaseModel as PydanticBaseModel,
)

try:
    import ujson as json
except ImportError:
    import json

__all__ = ['Model']


class Model(PydanticBaseModel):
    """基类"""

    def __new__(cls, *args, **kwargs):
        cls.update_forward_refs()
        return super(Model, cls).__new__(cls)

    class Config(PydanticBaseConfig):
        # 使用 ujson 作为解析库
        json_dumps = json.dumps
        json_loads = json.loads
