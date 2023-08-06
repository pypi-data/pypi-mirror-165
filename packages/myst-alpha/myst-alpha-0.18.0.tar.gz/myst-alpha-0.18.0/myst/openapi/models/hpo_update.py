from typing import Optional, Union

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.absolute_timing_create import AbsoluteTimingCreate
from myst.openapi.models.cron_timing_create import CronTimingCreate
from myst.openapi.models.hyperopt_create import HyperoptCreate
from myst.openapi.models.relative_timing_create import RelativeTimingCreate
from myst.openapi.models.search_space import SearchSpace


class HPOUpdate(base_model.BaseModel):
    """HPO schema for update input."""

    object_: Optional[Literal["HPO"]] = Field(..., alias="object")
    title: Optional[str] = None
    model: Optional[str] = None
    search_space: Optional[SearchSpace] = None
    test_start_time: Optional[str] = None
    test_end_time: Optional[str] = None
    fit_start_timing: Optional[Union[AbsoluteTimingCreate, RelativeTimingCreate]] = None
    fit_end_timing: Optional[Union[AbsoluteTimingCreate, RelativeTimingCreate]] = None
    fit_reference_timing: Optional[Union[AbsoluteTimingCreate, CronTimingCreate]] = None
    predict_start_timing: Optional[Union[AbsoluteTimingCreate, RelativeTimingCreate]] = None
    predict_end_timing: Optional[Union[AbsoluteTimingCreate, RelativeTimingCreate]] = None
    predict_reference_timing: Optional[CronTimingCreate] = None
    search_algorithm: Optional[HyperoptCreate] = None
    description: Optional[str] = None
