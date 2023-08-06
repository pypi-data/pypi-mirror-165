from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.connector_get_parameters_schema import ConnectorGetParametersSchema
from myst.openapi.models.connector_get_type import ConnectorGetType


class ConnectorGet(base_model.BaseModel):
    """Abstract base connector schema for get responses."""

    object_: Literal["Connector"] = Field(..., alias="object")
    type: ConnectorGetType
    uuid: str
    title: str
    provider: str
    description: str
    parameters_schema: ConnectorGetParametersSchema
    icon_url: Optional[str] = None
