from typing import Optional

from pydantic import Field
from typing_extensions import Literal

from myst.models import base_model
from myst.openapi.models.backtest_result_get_metrics import BacktestResultGetMetrics


class BacktestResultGet(base_model.BaseModel):
    """Schema for model fit result get responses."""

    object_: Literal["BacktestResult"] = Field(..., alias="object")
    uuid: str
    create_time: str
    start_time: str
    end_time: str
    result_url: str
    metrics: Optional[BacktestResultGetMetrics] = None
