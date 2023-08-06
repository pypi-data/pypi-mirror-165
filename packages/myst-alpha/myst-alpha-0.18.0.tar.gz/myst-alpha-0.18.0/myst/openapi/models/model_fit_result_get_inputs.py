from typing import Any, Dict, List

from myst.models import base_model
from myst.models.time_dataset import TimeDataset


class ModelFitResultGetInputs(base_model.BaseModel):
    """The data that was used to calculate this result."""

    __root__: Dict[str, List[TimeDataset]]

    def __getitem__(self, item: str) -> Any:
        return self.__root__[item]
