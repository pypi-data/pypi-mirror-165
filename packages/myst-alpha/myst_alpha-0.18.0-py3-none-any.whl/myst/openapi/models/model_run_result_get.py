from typing import List, Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.models.time_dataset import TimeDataset
from myst.openapi.models.model_run_result_get_inputs import ModelRunResultGetInputs


class ModelRunResultGet(base_model.BaseModel):
    """Schema for model run result get responses."""

    object_: Literal["NodeResult"] = Field(..., alias="object")
    uuid: str
    create_time: str
    type: Literal["ModelRunResult"]
    node: str
    start_time: str
    end_time: str
    as_of_time: str
    inputs: ModelRunResultGetInputs
    outputs: List[TimeDataset]
    update_time: Optional[str] = None
