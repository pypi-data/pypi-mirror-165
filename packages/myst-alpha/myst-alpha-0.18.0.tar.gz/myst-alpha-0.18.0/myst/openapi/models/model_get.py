from typing import List, Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.deploy_status import DeployStatus
from myst.openapi.models.model_get_input_specs_schema import ModelGetInputSpecsSchema
from myst.openapi.models.model_get_parameters import ModelGetParameters
from myst.openapi.models.time_dataset_spec import TimeDatasetSpec


class ModelGet(base_model.BaseModel):
    """Schema for model get responses."""

    object_: Literal["Node"] = Field(..., alias="object")
    uuid: str
    create_time: str
    organization: str
    owner: str
    type: Literal["Model"]
    title: str
    project: str
    creator: str
    deploy_status: DeployStatus
    connector_uuid: str
    parameters: ModelGetParameters
    input_specs_schema: ModelGetInputSpecsSchema
    update_time: Optional[str] = None
    description: Optional[str] = None
    output_specs: Optional[List[TimeDatasetSpec]] = None
