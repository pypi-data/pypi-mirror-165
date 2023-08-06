
from __future__ import annotations
from typing import Any, Optional

from galaxy2janis.gx.gxtool.param import BoolParam
from galaxy2janis.gx.gxtool.param import Param

from .InputComponent import InputComponent


class Flag(InputComponent):
    def __init__(self, prefix: str) -> None:
        super().__init__()
        self.prefix = prefix

    @property
    def name(self) -> str:
        return self.prefix.strip('--')

    @property
    def default_value(self) -> bool:
        if isinstance(self.gxparam, BoolParam):
            if self.gxparam.checked and self.gxparam.truevalue == self.prefix:
                return True
            elif self.gxparam.checked and self.gxparam.truevalue == "":
                return False
            elif not self.gxparam.checked and self.gxparam.falsevalue == self.prefix:
                return True
            elif not self.gxparam.checked and self.gxparam.falsevalue == "":
                return False
        return False
    
    @property
    def optional(self) -> bool:
        return True

    @property
    def array(self) -> bool:
        return False

    @property
    def docstring(self) -> Optional[str]:
        if self.gxparam:
            return self.gxparam.docstring
        return None

    def update(self, incoming: Any):
        assert(isinstance(incoming, Flag))
        # gxparam transfer
        if not self.gxparam and incoming.gxparam:
            self.gxparam: Optional[Param] = incoming.gxparam
        
    def __str__(self) -> str:
        return f'{str(self.default_value):20}{str(self.optional):>10}'
