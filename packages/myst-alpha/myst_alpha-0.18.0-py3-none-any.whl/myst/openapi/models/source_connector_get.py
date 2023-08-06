from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.source_connector_get_parameters_schema import SourceConnectorGetParametersSchema


class SourceConnectorGet(base_model.BaseModel):
    """Schema for source connector get responses."""

    object_: Literal["Connector"] = Field(..., alias="object")
    type: Literal["SourceConnector"]
    uuid: str
    title: str
    provider: str
    description: str
    parameters_schema: SourceConnectorGetParametersSchema
    icon_url: Optional[str] = None
