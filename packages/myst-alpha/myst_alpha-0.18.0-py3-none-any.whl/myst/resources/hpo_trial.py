import json
from typing import Any, Dict, Optional

import httpx
import pandas as pd
from pydantic import BaseModel

from myst.resources.utils import backtest_result_to_pandas_data_frame


def _download_result(result_url: str) -> Dict[str, Any]:
    """Downloads the backtest result from the supplied URL and parses it."""
    response = httpx.get(result_url)

    if response.status_code == 200:
        result_data = json.loads(response.content)
    else:
        raise RuntimeError("Could not download backtest result.")

    return result_data


class HPOTrial(BaseModel):
    parameters: Dict[str, Any]
    metrics: Dict[str, float]
    create_time: Optional[str] = None
    backtest_result_url: Optional[str] = None

    # TODO(CRYS-3649): move `backtest_result_to_pandas_data_frame` logic out of client.
    def to_pandas_data_frame(self) -> pd.DataFrame:
        """Downloads the HPO result and converts the time arrays to pandas data frames.

        Data will be re-indexed against the predictions' natural time index, dropping any target data that doesn't
        correspond to a prediction.

        Returns:
            a pandas data frame with the predictions made by the HPO, and their corresponding targets. # noqa: DAR202

        Raises:
            ValueError: if missing `backtest_result_url`
        """
        if self.backtest_result_url is None:
            raise ValueError("No result url saved for this `HPOTrial`.")

        result_data = _download_result(result_url=self.backtest_result_url)
        pandas_data_frame = backtest_result_to_pandas_data_frame(result_data=result_data)

        return pandas_data_frame
