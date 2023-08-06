from typing import Any, Dict, Union

from myst.models import base_model


class TimeDatasetMetadata(base_model.BaseModel):
    """User-defined metadata about the time dataset."""

    __root__: Dict[str, Union[bool, float, int, str]]

    def __getitem__(self, item: str) -> Any:
        return self.__root__[item]
