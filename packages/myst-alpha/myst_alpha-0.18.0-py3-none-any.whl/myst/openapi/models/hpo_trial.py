from typing import Optional

from myst.models import base_model
from myst.openapi.models.hpo_trial_metrics import HPOTrialMetrics
from myst.openapi.models.hpo_trial_parameters import HPOTrialParameters


class HPOTrial(base_model.BaseModel):
    """Represents the result of a single HPO trial."""

    parameters: HPOTrialParameters
    metrics: HPOTrialMetrics
    create_time: str
    backtest_result_url: Optional[str] = None
