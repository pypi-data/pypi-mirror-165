import warnings
from typing import Any, Dict

import pandas as pd

from myst.models.time_dataset import TimeDataset


def backtest_result_to_pandas_data_frame(result_data: Dict[str, Any]) -> pd.DataFrame:
    """Converts backtest result to pandas data frames.

    Data will be re-indexed against the predictions' natural time index, dropping any target data that doesn't
    correspond to a prediction.

    Args:
        result_data: result data

    Returns:
        a pandas data frame with the predictions made by the backtest, and their corresponding targets

    Raises:
        NotImplementedError: for result data with more than one target
    """

    # Assume that there is only one target for now.
    if len(result_data["targets"]) != 1:
        raise NotImplementedError

    # Aggregate all predictions into a list of data frames, setting the index to both `time` and `reference_time`.
    prediction_pandas_objects = []
    for fold in result_data["fold_results"]:
        for predict_result in fold["predict_results"]:
            for prediction in predict_result["predictions"]:
                prediction_time_dataset = TimeDataset.parse_obj(prediction)
                # Disable an argument deprecated warning.
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore",
                        category=FutureWarning,
                        message="Argument `closed` is deprecated in favor of `inclusive`.",
                    )
                    prediction_pandas_object = prediction_time_dataset.flatten().to_pandas_object()

                multi_index = pd.MultiIndex.from_product(
                    [prediction_pandas_object.index, [pd.Timestamp(predict_result["reference_time"])]],
                    names=["time", "reference_time"],
                )
                prediction_pandas_objects.append(prediction_pandas_object.set_axis(multi_index, inplace=False))

    # Create the prediction data frame.
    prediction_pandas_object = pd.concat(prediction_pandas_objects)

    # Create the target data frame.
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", category=FutureWarning, message="Argument `closed` is deprecated in favor of `inclusive`."
        )
        target_pandas_object = TimeDataset.parse_obj(result_data["targets"][0]).flatten().to_pandas_object()

    # Re-index the target data frame against the `time` index of the predictions, ensuring that we can make a
    # combined data frame with a single natural time index.
    target_pandas_object = target_pandas_object.reindex(
        prediction_pandas_object.index.get_level_values("time")
    ).set_axis(prediction_pandas_object.index, inplace=False)

    # Cast `target_pandas_object` as a `pd.DataFrame` if `prediction_pandas_object` is a `pd.DataFrame`. Then add
    # empty string columns to the `target_pandas_object` dataframe. We do this
    # to cleanly merge `prediction_pandas_object`'s `pd.MultiIndex` columns.
    if isinstance(prediction_pandas_object, pd.DataFrame) and isinstance(target_pandas_object, pd.Series):
        target_column_names = tuple("" for _ in range(prediction_pandas_object.columns.nlevels))
        target_pandas_object = target_pandas_object.to_frame(name=target_column_names)
        target_pandas_object.columns.names = prediction_pandas_object.columns.names

    # Return the combined data frame.
    pandas_data_frame = pd.concat(
        [target_pandas_object, prediction_pandas_object], axis=1, keys=["targets", "predictions"]
    )

    return pandas_data_frame
