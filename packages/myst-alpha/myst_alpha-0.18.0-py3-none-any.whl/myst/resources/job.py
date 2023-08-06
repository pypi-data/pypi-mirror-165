import time
from typing import TYPE_CHECKING, List, Optional, Union
from uuid import UUID

from myst import get_client
from myst.adapters.utils import get_resource_uuid
from myst.models.types import UUIDOrStr
from myst.openapi.api.projects.models.fit_jobs import get_models_fit_job
from myst.openapi.api.projects.time_series.run_jobs import get_time_series_run_job
from myst.openapi.models.job_error import JobError
from myst.openapi.models.job_state import JobState
from myst.resources.resource import Resource

if TYPE_CHECKING:  # Avoid circular imports.
    from myst.resources.model import Model
    from myst.resources.project import Project
    from myst.resources.time_series import TimeSeries


class NodeJob(Resource):
    """Describes a job associated with a node.

    Attributes:
        project: the UUID of the project this job corresponds to
        node: the UUID of the node this job corresponds to
        start_timing: the beginning of the natural time range for which this job applies, inclusive
        end_timing: the end of the natural time range for which this job applies, exclusive
        as_of_time: the as of time of this job applies
        result: the UUID of the optional result this job corresponds to
        errors: a list of errors associated with this job
        state: job state
    """

    project: UUID
    node: UUID
    start_time: str
    end_time: str
    as_of_time: str
    result: Optional[UUID]
    errors: List[JobError]
    state: JobState

    def is_completed(self) -> bool:
        """Returns `True` if the job has completed.

        Completed jobs include both successful and failed jobs.

        Returns:
            whether the job has completed
        """
        return self.state in [JobState.SUCCESS, JobState.FAILURE, JobState.UPSTREAM_FAILURE]


class TimeSeriesRunJob(NodeJob):
    """Describes a node run job on a time series."""

    @classmethod
    def get(
        cls, project: Union["Project", UUIDOrStr], time_series: Union["TimeSeries", UUIDOrStr], uuid: UUIDOrStr
    ) -> "TimeSeriesRunJob":
        """Gets a specific time series run job by its identifier."""
        time_series_job = get_time_series_run_job.request_sync(
            client=get_client(),
            project_uuid=str(get_resource_uuid(project)),
            time_series_uuid=str(get_resource_uuid(time_series)),
            uuid=str(uuid),
        )

        return TimeSeriesRunJob.parse_obj(dict(time_series_job.dict(), project=get_resource_uuid(project)))

    def wait_until_completed(self) -> "TimeSeriesRunJob":
        """Returns the job once it has completed."""
        while True:
            refreshed_job = TimeSeriesRunJob.get(project=self.project, time_series=self.node, uuid=self.uuid)

            if refreshed_job.is_completed():
                break

            time.sleep(60)

        return TimeSeriesRunJob.parse_obj(dict(refreshed_job.dict(), project=self.project))


class ModelFitJob(NodeJob):
    """Describes a model fit job on a model."""

    @classmethod
    def get(
        cls, project: Union["Project", UUIDOrStr], model: Union["Model", UUIDOrStr], uuid: UUIDOrStr
    ) -> "ModelFitJob":
        """Gets a specific model fit job by its identifier."""
        model_job = get_models_fit_job.request_sync(
            client=get_client(),
            project_uuid=str(get_resource_uuid(project)),
            model_uuid=str(get_resource_uuid(model)),
            uuid=str(uuid),
        )

        return ModelFitJob.parse_obj(dict(model_job.dict(), project=get_resource_uuid(project)))

    def wait_until_completed(self) -> "ModelFitJob":
        """Returns the job once it has completed."""
        while True:
            refreshed_job = ModelFitJob.get(project=self.project, model=self.node, uuid=self.uuid)

            if refreshed_job.is_completed():
                break

            time.sleep(60)

        return ModelFitJob.parse_obj(dict(refreshed_job.dict(), project=self.project))
