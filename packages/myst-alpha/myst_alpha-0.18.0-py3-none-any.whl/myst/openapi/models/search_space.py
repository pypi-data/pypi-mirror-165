from typing import Any, Dict, Union

from myst.models import base_model
from myst.openapi.models.choice import Choice
from myst.openapi.models.constant import Constant
from myst.openapi.models.log_uniform import LogUniform
from myst.openapi.models.q_log_uniform import QLogUniform
from myst.openapi.models.q_uniform import QUniform
from myst.openapi.models.uniform import Uniform


class SearchSpace(base_model.BaseModel):
    """"""

    __root__: Dict[str, Union[Choice, Constant, LogUniform, QLogUniform, QUniform, Uniform]]

    def __getitem__(self, item: str) -> Any:
        return self.__root__[item]
