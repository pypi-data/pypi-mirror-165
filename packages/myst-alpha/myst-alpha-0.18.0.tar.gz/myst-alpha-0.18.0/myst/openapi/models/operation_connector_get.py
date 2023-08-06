from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.operation_connector_get_parameters_schema import OperationConnectorGetParametersSchema


class OperationConnectorGet(base_model.BaseModel):
    """Schema for operation connector get responses."""

    object_: Literal["Connector"] = Field(..., alias="object")
    type: Literal["OperationConnector"]
    uuid: str
    title: str
    provider: str
    description: str
    parameters_schema: OperationConnectorGetParametersSchema
    icon_url: Optional[str] = None
