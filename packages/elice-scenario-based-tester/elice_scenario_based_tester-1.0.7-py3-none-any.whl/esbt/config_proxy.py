import hashlib
from functools import cached_property
from typing import Any, Dict, List, Optional

import msgpack
from ebc.config_proxy import load_config
from pydantic import BaseModel

__all__ = ['config']


class ConfigTemplate(BaseModel):
    SERVER_API: str
    
    WAIT_FOR_SCENARIO_TIMEOUT: int

    FINISHED_SUFFIX: str
    REPEAT_CNT_SUFFIX: str

    RESPONSE_VALIDATE_FIELD: str

    FORM_DATA_CONTENT_TYPE: str

    RFC_KEYS: Dict[str, str]

    @cached_property
    def ident(self) -> str:
        return hashlib.sha256(msgpack.packb(self.dict())).hexdigest()

    class Config:
        allow_mutation = False
        keep_untouched = (cached_property,)


config = ConfigTemplate.parse_obj(load_config().items())
