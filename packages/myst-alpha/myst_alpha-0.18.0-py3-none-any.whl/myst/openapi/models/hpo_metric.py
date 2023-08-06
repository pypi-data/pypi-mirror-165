from enum import Enum


class HPOMetric(str, Enum):
    MAE = "mae"
    MAPE = "mape"
    MEAN_NEGATIVE_LOG_LIKELIHOOD = "mean_negative_log_likelihood"
    MEAN_PINBALL_LOSS = "mean_pinball_loss"
    MSE = "mse"
    RMSE = "rmse"

    def __str__(self) -> str:
        return str(self.value)
