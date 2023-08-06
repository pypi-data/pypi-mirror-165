import json
from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Union

import httpx
import pandas as pd

from myst.adapters.utils import get_resource_uuid
from myst.client import get_client
from myst.core.time.time import Time
from myst.models.types import UUIDOrStr
from myst.openapi.api.projects.backtests.results import get_backtest_result
from myst.resources.backtest_job import BacktestJob
from myst.resources.resource import Resource
from myst.resources.utils import backtest_result_to_pandas_data_frame

if TYPE_CHECKING:  # Avoid circular imports.
    from myst.resources.backtest import Backtest
    from myst.resources.project import Project


def _download_result(result_url: str) -> Dict[str, Any]:
    """Downloads the backtest result from the supplied URL and parses it."""
    response = httpx.get(result_url)

    if response.status_code == 200:
        result_data = json.loads(response.content)
    else:
        raise RuntimeError("Could not download backtest result.")

    return result_data


class BacktestResult(Resource):

    start_time: Time
    end_time: Time
    result_url: str
    metrics: Optional[Mapping[str, Optional[float]]]

    @classmethod
    def get(
        cls,
        project: Union["Project", UUIDOrStr],
        backtest: Union["Backtest", UUIDOrStr],
        job: Union[BacktestJob, UUIDOrStr],
    ) -> "BacktestResult":
        backtest_result = get_backtest_result.request_sync(
            client=get_client(),
            project_uuid=str(get_resource_uuid(project)),
            backtest_uuid=str(get_resource_uuid(backtest)),
            job_uuid=str(job.uuid) if isinstance(job, BacktestJob) else str(job),
        )

        return BacktestResult.parse_obj(backtest_result.dict())

    # TODO(CRYS-3649): move `backtest_result_to_pandas_data_frame` logic out of client.
    def to_pandas_data_frame(self) -> pd.DataFrame:
        """Downloads the backtest result and converts the time arrays to pandas data frames.

        Data will be re-indexed against the predictions' natural time index, dropping any target data that doesn't
        correspond to a prediction.

        Returns:
            a pandas data frame with the predictions made by the backtest, and their corresponding targets
        """
        result_data = _download_result(result_url=self.result_url)
        pandas_data_frame = backtest_result_to_pandas_data_frame(result_data=result_data)

        return pandas_data_frame
