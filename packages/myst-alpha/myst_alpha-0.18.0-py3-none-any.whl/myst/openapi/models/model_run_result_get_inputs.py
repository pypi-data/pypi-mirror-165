from typing import Any, Dict, List

from myst.models import base_model
from myst.models.time_dataset import TimeDataset


class ModelRunResultGetInputs(base_model.BaseModel):
    """The input data that was used to create the outputs of this result."""

    __root__: Dict[str, List[TimeDataset]]

    def __getitem__(self, item: str) -> Any:
        return self.__root__[item]
