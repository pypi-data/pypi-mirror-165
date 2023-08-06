from typing import Optional, Union

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.absolute_timing_create import AbsoluteTimingCreate
from myst.openapi.models.relative_timing_create import RelativeTimingCreate


class NodeJobCreate(base_model.BaseModel):
    """Abstract base job schema for create post."""

    object_: Literal["NodeJob"] = Field(..., alias="object")
    start_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    end_timing: Union[AbsoluteTimingCreate, RelativeTimingCreate]
    as_of_time: Optional[AbsoluteTimingCreate] = None
