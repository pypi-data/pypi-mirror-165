import enum
from typing import Optional
from uuid import UUID

from myst.connectors.model_connector import ModelConnector


@enum.unique
class GroupName(str, enum.Enum):
    FEATURES = "features"
    TARGETS = "targets"
    SAMPLE_WEIGHTS = "sample_weights"


@enum.unique
class LogisticRegressionPenalty(str, enum.Enum):
    ELASTIC_NET = "elasticnet"
    L1 = "l1"
    L2 = "l2"
    NONE = "none"


@enum.unique
class LogisticRegressionSolver(str, enum.Enum):
    LBFGS = "lbfgs"
    LIBLINEAR = "liblinear"
    NEWTON_CG = "newton-cg"
    SAG = "sag"
    SAGA = "saga"


class LogisticRegression(ModelConnector):
    def __init__(
        self,
        penalty: Optional[LogisticRegressionPenalty] = None,
        constraint: Optional[float] = None,
        fit_intercept: Optional[bool] = None,
        solver: Optional[LogisticRegressionSolver] = None,
        max_iter: Optional[int] = None,
        l1_ratio: Optional[float] = None,
    ) -> None:
        super().__init__(
            uuid=UUID("789b7a82-2ae4-4a9c-8078-dfa9d14b120b"),
            parameters=dict(
                penalty=penalty,
                constraint=constraint,
                fit_intercept=fit_intercept,
                solver=solver,
                max_iter=max_iter,
                l1_ratio=l1_ratio,
            ),
        )
